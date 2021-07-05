import logging
from ReverseProxyServer import ProxyHTTPServer
from ReverseProxyServer import SimpleProxyHTTPRequestHandler

log = logging.getLogger(__name__)

def main():
	try:
		server_address = ('0.0.0.0', 8008)
		with ProxyHTTPServer(server_address, SimpleProxyHTTPRequestHandler) as httpr:
			log.warning(f'Access server on.. http(s)://{server_address[0]}:{server_address[1]}/')
			httpr.serve_forever()
	except KeyboardInterrupt:
		log.warning('CTRL+C Detected!')

if __name__ == '__main__':
	main()

# end-of-file