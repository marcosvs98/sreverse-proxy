from abc import ABC, abstractmethod

class ProxyForwardingHeaders(ABC):
	def __init__(self, original):
		self.original = original if original else []
		self.keep_headers = []
		self.added_headers = []
		self.remove_headers = []

	def set(self, headers):
		self.original = headers

	def keep(self, name):
		self.keep_headers.append(name)

	def add(self, name, value):
		self.added_headers.append((name, value))

	def remove(self, name):
		self.remove_headers.append(name)

	def reset(self):
		self.add.clear()
		self.keep_headers.clear()
		self.remove.clear()

	def should_keep(self, name):
		for keep in self.keep_headers:
			if name.lower() == keep.lower():
				return True
		return False

	def should_remove(self, name):
		for keep in self.remove_headers:
			if name.lower() == keep.lower():
				return True
		return False

	@abstractmethod
	def get(self):
		pass


class ProxyForwardingRequestHeaders(ProxyForwardingHeaders):
	def get(self):
		foward_headers = []

		for k, v in self.added_headers:
			foward_headers.append((k, v))

		for k, v in self.original:
			if self.should_remove(k):
				continue
			elif self.should_keep(k):
				foward_headers.append((k, v))
			elif not k.startswith('X-Proxy-'):
				foward_headers.append((k, v))
		return foward_headers


class ProxyForwardingResponseHeaders(ProxyForwardingHeaders):

	def __init__(self, original=None, caching=True):
		self.caching = caching
		super(ProxyForwardingResponseHeaders, self).__init__(original)

	def get(self):
		foward_headers = []

		for k, v in self.original:
			if self.should_remove(k):
				continue
			if self.should_keep(k):
				foward_headers.append((k,v))

		if self.caching:
			foward_headers.append(('Cache-Control', 'no-cache, no-store, must-revalidate'))
			foward_headers.append(('Expires', 'Thu, 01 Jan 1970 00:00:00 GMT'))
			foward_headers.append(('Pragma', 'no-cache'))

		for k, v in self.added_headers:
			if not k.startswith('X-Proxy-'):
				foward_headers.append((k, v))

		for k, v in self.original:
			if self.should_remove(k):
				continue
			if self.should_keep(k):
				continue
			foward_headers.append((f'X-Forwarded-{k}', v))

		for k, v in self.added_headers:
			if k.startswith('X-Proxy-'):
				foward_headers.append((k, v))

		return foward_headers


# end-of-file