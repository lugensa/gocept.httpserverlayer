from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
import os
import plone.testing
import threading
import wsgiref.handlers


class LogWSGIRequestHandler(WSGIRequestHandler):

    def log_request(self, *args):
        if 'GOCEPT_HTTP_VERBOSE_LOGGING' in os.environ:
            WSGIRequestHandler.log_request(self, *args)


class Layer(plone.testing.Layer):

    port = 0  # choose automatically
    request_handler_class = LogWSGIRequestHandler

    def __init__(self, *args, **kw):
        super(Layer, self).__init__(*args, **kw)
        self.wsgi_app = None

    @property
    def wsgi_app(self):
        return self.get('wsgi_app', self._wsgi_app)

    @wsgi_app.setter
    def wsgi_app(self, value):
        self._wsgi_app = value

    @property
    def host(self):
        return os.environ.get('GOCEPT_HTTP_APP_HOST', 'localhost')

    def setUp(self):
        self['httpd'] = WSGIServer((self.host, self.port),
                                   self.request_handler_class)
        port = self['httpd'].server_port
        self['http_host'] = self.host
        self['http_port'] = port
        self['http_address'] = '%s:%s' % (self.host, port)
        self['httpd'].set_app(self.wsgi_app)
        self['httpd_thread'] = threading.Thread(target=self.serve)
        self['httpd_thread'].daemon = True
        self['httpd_thread'].start()

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
        self.shutdown()
        self['httpd_thread'].join(5)
        if self['httpd_thread'].isAlive():
            raise RuntimeError('WSGI server could not be shut down')
        # make the server really go away and give up the socket
        del self['httpd']
        del self['httpd_thread']

        del self['http_host']
        del self['http_port']
        del self['http_address']

        wsgiref.handlers.SimpleHandler._flush = self['_orig_handler_flush']
        del self['_orig_handler_flush']

    def serve(self):
        self['httpd'].serve_forever()

    def shutdown(self):
        self['httpd'].shutdown()
        self['httpd'].server_close()


class FixupMiddleware(object):
    """Fix problems between WSGI server and middlewares."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # gocept.httpserverlayer uses wsgiref but
        # wsgiref.simple_server.ServerHandler.start_response bails when it
        # sees the 'Connection' header, so we remove it here:
        def clean_start_response(status, headers, exc_info):
            headers = [(k, v) for (k, v) in headers if k != 'Connection']
            return start_response(status, headers, exc_info)

        return self.app(environ, clean_start_response)
