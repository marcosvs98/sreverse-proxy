import urllib3
import logging
from types import SimpleNamespace
from dataclasses import dataclass
from urllib.parse import urlparse, urljoin
from urllib.parse import urlencode, urlunparse, parse_qs
from urllib.parse import quote, unquote, quote_plus, urlparse
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from socketserver import ForkingMixIn, ThreadingMixIn
from ProxyForwardingHeaders import ProxyForwardingRequestHeaders
from ProxyForwardingHeaders import ProxyForwardingResponseHeaders

log = logging.getLogger('reverse-srever_proxy')

@dataclass
class ProxyRequest:

	source_address : str
	path           : str
	method         : str
	headers        : list
	postdata       : bytes = None
	http_version   : str = 'HTTP/1.0'


class ProxyHTTPServer(ThreadingMixIn, HTTPServer):
	block_on_close = True
	allow_reuse_address = True


class SimpleProxyHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self._request()

	def do_POST(self):
		self._request()

	def log_request(self, code=None, size=None):
		log.warning(f'status="{code}" path="{self.path}"')

	def get_forward_request_headers(self):
		header = ProxyForwardingRequestHeaders(self.headers.items())
		url = urlparse(self.url)
		header.remove('Host')
		header.add('Host', url.netloc)
		return header.get()

	def on_proxy_response(self, request, fwrequest, fwresponse):
		header = ProxyForwardingResponseHeaders(fwresponse.headers.items())
		header.keep('Content-Type')
		header.keep('Content-Language')
		header.keep('Content-Length')
		header.keep('Content-Encoding')
		header.add('X-Proxy-Redirect-Count', fwresponse.retries.total)
		header.add('X-Proxy-Forward-Location', fwrequest.url)
		fwresponse.headers = header.get()

	def _request(self):
		try:
			http_client = urllib3.PoolManager()
			parsed = urlparse(self.path)
			qs = (parse_qs(unquote(parsed.query))).get("url")
			if qs:
				self.url = qs[0]
			
			proxy_request = ProxyRequest(
				source_address=self.client_address[0],
				http_version=self.request_version,
				method=self.command,
				path=self.path,
				headers=self.headers.items()
			)
			foward_request = SimpleNamespace(
				method=proxy_request.method,
				url=self.url,
				headers=proxy_request.headers[:])
			foward_request.headers = self.get_forward_request_headers()
			foward_response = http_client.request(foward_request.method, foward_request.url)
			self.on_proxy_response(proxy_request, foward_request, foward_response)
			self.send_response(foward_response.status)
			for header in foward_response.headers:
				self.send_header(*header)
			self.end_headers()
			self.wfile.write(foward_response.data)
		except urllib3.exceptions.LocationValueError as e:
			log.error(e)
		except ConnectionError as e:
			log.error(f'Connection closed unexpectedly: {repr(e)}')
		except IOError as e:
			log.error(f'An input/output error has occurred: {repr(e)}')

# end-of-file
