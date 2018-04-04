try:
    import BaseHTTPServer as http_server
except ImportError:
    import http.server as http_server
import plone.testing
import threading
import time
import wsgiref.handlers


class Layer(plone.testing.Layer):

    host = 'localhost'
    port = 0  # choose automatically

    def __init__(self, request_handler=None, *args, **kw):
        super(Layer, self).__init__(*args, **kw)
        self.request_handler = request_handler

    def setUp(self):
        self['request_handler'] = self.request_handler
        self['httpd'] = http_server.HTTPServer(
            (self.host, self.port), self.request_handler)
        self['httpd_thread'] = threading.Thread(
            target=self['httpd'].serve_forever)
        self['httpd_thread'].daemon = True
        self['httpd_thread'].start()
        # Wait as it sometimes takes a while to get the server started.
        # XXX this is a little kludgy
        time.sleep(0.001)
        port = self['httpd'].server_port
        self['http_host'] = self.host
        self['http_port'] = port
        self['http_address'] = '%s:%s' % (self.host, port)

        # XXX copy&paste from gocept.httpserverlayer.wsgi
        orig_flush = self['_orig_handler_flush'] = (
            wsgiref.handlers.SimpleHandler._flush)

        def silent_flush(self):
            try:
                orig_flush(self)
            except OSError as e:
                if e.args[0] != 32:
                    raise

        wsgiref.handlers.SimpleHandler._flush = silent_flush

    def tearDown(self):
        self['httpd'].shutdown()
        self['httpd'].server_close()
        self['httpd_thread'].join()
        del self['request_handler']
        del self['httpd']
        del self['httpd_thread']
        del self['http_host']
        del self['http_port']
        del self['http_address']

        wsgiref.handlers.SimpleHandler._flush = self['_orig_handler_flush']
        del self['_orig_handler_flush']


class RequestHandler(http_server.BaseHTTPRequestHandler):
    """Handler for testing which does not log to STDOUT."""

    def log_message(self, format, *args):
        pass
