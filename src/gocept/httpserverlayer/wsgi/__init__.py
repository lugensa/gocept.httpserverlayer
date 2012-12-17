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
