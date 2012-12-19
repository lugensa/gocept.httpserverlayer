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

    host = 'localhost'
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

    def setUp(self):
        self.http = WSGIServer((self.host, self.port),
                               self.request_handler_class)
        self.port = self.http.server_port
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)
        self.http.set_app(self.wsgi_app)
        self.thread = threading.Thread(target=self.serve)
        self.thread.daemon = True
        self.thread.start()

    def tearDown(self):
        self.shutdown()
        self.thread.join(5)
        if self.thread.isAlive():
            raise RuntimeError('WSGI server could not be shut down')
        # make the server really go away and give up the socket
        self.http = None

    def serve(self):
        if hasattr(self.http, 'shutdown'):
            self.http.serve_forever()
        else:
            # python < 2.6
            self._running = True
            while self._running:
                self.http.handle_request()

    def shutdown(self):
        if hasattr(self.http, 'shutdown'):
            self.http.shutdown()
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
