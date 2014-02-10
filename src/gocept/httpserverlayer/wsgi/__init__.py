from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
import os
import plone.testing
import socket
import threading
import urllib


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

    def _get_wsgi_app(self):
        return self.get('wsgi_app', self._wsgi_app)

    def _set_wsgi_app(self, value):
        self._wsgi_app = value

    wsgi_app = property(_get_wsgi_app, _set_wsgi_app)

    @property
    def host(self):
        return os.environ.get('GOCEPT_HTTP_APP_HOST', 'localhost')

    def setUp(self):
        self['httpd'] = WSGIServer((self.host, self.port),
                               self.request_handler_class)
        self.port = self['httpd'].server_port
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)
        self['httpd'].set_app(self.wsgi_app)
        self['httpd_thread'] = threading.Thread(target=self.serve)
        self['httpd_thread'].daemon = True
        self['httpd_thread'].start()

        def silent_flush(self):
            try:
                orig_flush(self)
            except socket.error, e:
                if e.args[0] != 32:
                    raise
        orig_flush = self['_orig_socket_flush'] = socket._fileobject.flush
        socket._fileobject.flush = silent_flush

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

        socket._fileobject.flush = self['_orig_socket_flush']
        del self['_orig_socket_flush']

    def serve(self):
        if hasattr(self['httpd'], 'shutdown'):
            self['httpd'].serve_forever()
        else:
            # python < 2.6
            self._running = True
            while self._running:
                self['httpd'].handle_request()

    def shutdown(self):
        if hasattr(self['httpd'], 'shutdown'):
            self['httpd'].shutdown()
        else:
            # python < 2.6
            self._running = False
            try:
                urllib.urlopen('http://%s:%s/die' % (self.host, self.port))
            except socket.error:
                pass


class FixupMiddleware(object):
    """Fix problems between WSGI server and middlewares."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # wsgiref.simple_server.ServerHandler.setup_environ adds
        # 'CONTENT_LENGTH' key to environ which has the value '', but
        # repoze.retry.Retry.__call__ 1.0. expects the value to be
        # convertable to `int` See http://bugs.repoze.org/issue171.
        if environ.get('CONTENT_LENGTH') == '':
            del environ['CONTENT_LENGTH']

        # gocept.httpserverlayer uses wsgiref but
        # wsgiref.simple_server.ServerHandler.start_response bails when it
        # sees the 'Connection' header, so we remove it here:
        def clean_start_response(status, headers, exc_info):
            headers = [(k, v) for (k, v) in headers if k != 'Connection']
            return start_response(status, headers, exc_info)

        return self.app(environ, clean_start_response)
