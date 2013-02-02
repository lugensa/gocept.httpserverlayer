import BaseHTTPServer
import threading
import time
import plone.testing
import urllib2


class HTTPServer(BaseHTTPServer.HTTPServer):

    _continue = True

    def __init__(self, *args):
        BaseHTTPServer.HTTPServer.__init__(self, *args)
        self.errors = []

    def handle_error(self, request, client_address):
        self.errors.append((request, client_address))

    def serve_until_shutdown(self):
        while self._continue:
            self.handle_request()

    def shutdown(self):
        self._continue = False
        # We fire a last request at the server in order to take it out of the
        # while loop in `self.serve_until_shutdown`.
        try:
            urllib2.urlopen(
                'http://%s:%s/tearDown' % (self.server_name, self.server_port),
                timeout=1)
        except urllib2.URLError:
            # If the server is already shut down, we receive a socket error,
            # which we ignore.
            pass
        self.server_close()


class Layer(plone.testing.Layer):

    host = 'localhost'
    port = 0  # choose automatically

    def __init__(self, request_handler=None, *args, **kw):
        super(Layer, self).__init__(*args, **kw)
        self.request_handler = request_handler

    def setUp(self):
        self['request_handler'] = self.request_handler
        self['httpd'] = HTTPServer(
            (self.host, self.port), self.request_handler)
        self.thread = threading.Thread(
            target=self['httpd'].serve_until_shutdown)
        self.thread.daemon = True
        self.thread.start()
        # Wait as it sometimes takes a while to get the server started.
        # XXX this is a little kludgy
        time.sleep(0.001)
        self.port = self['httpd'].server_port
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)

    def tearDown(self):
        self['httpd'].shutdown()
        self.thread.join()
        del self['request_handler']
        del self['httpd']

    def testTearDown(self):
        self['httpd'].errors[:] = []


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Handler for testing which does not log to STDOUT."""

    def log_message(self, format, *args):
        pass
