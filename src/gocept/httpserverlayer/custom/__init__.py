import BaseHTTPServer
import threading
import time
import plone.testing


class Layer(plone.testing.Layer):

    host = 'localhost'
    port = 0  # choose automatically

    def __init__(self, request_handler=None, *args, **kw):
        super(Layer, self).__init__(*args, **kw)
        self.request_handler = request_handler

    def setUp(self):
        self['request_handler'] = self.request_handler
        self['httpd'] = BaseHTTPServer.HTTPServer(
            (self.host, self.port), self.request_handler)
        self['httpd_thread'] = threading.Thread(
            target=self['httpd'].serve_forever)
        self['httpd_thread'].daemon = True
        self['httpd_thread'].start()
        # Wait as it sometimes takes a while to get the server started.
        # XXX this is a little kludgy
        time.sleep(0.001)
        self.port = self['httpd'].server_port
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)

    def tearDown(self):
        self['httpd'].shutdown()
        self['httpd_thread'].join()
        del self['request_handler']
        del self['httpd']
        del self['httpd_thread']
        del self['http_host']
        del self['http_port']
        del self['http_address']


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Handler for testing which does not log to STDOUT."""

    def log_message(self, format, *args):
        pass
