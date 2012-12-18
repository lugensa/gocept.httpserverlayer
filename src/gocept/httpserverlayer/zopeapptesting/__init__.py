from zope.server.taskthreads import ThreadedTaskDispatcher
import asyncore
import plone.testing
import threading
import time
import zope.app.server.wsgi
import zope.app.testing.functional
import zope.app.wsgi


class Layer(plone.testing.Layer):

    host = 'localhost'
    port = 0  # choose automatically

    def setUp(self):
        task_dispatcher = ThreadedTaskDispatcher()
        task_dispatcher.setThreadCount(1)
        db = zope.app.testing.functional.FunctionalTestSetup().db
        self.http = zope.app.server.wsgi.http.create(
            'WSGI-HTTP', task_dispatcher, db,
            ip=self.host, port=self.port)
        self.thread = threading.Thread(target=self.run_server)
        self.thread.setDaemon(True)
        self.thread.start()
        time.sleep(0.025)
        _, self.port = self.http.socket.getsockname()
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)

    def tearDown(self):
        self.running = False
        self.thread.join()

    def run_server(self):
        self.running = True
        while self.running:
            asyncore.poll(0.1)
        self.http.close()


class TestCase(zope.app.testing.functional.FunctionalTestCase):

    def setUp(self):
        # switches the HTTP-server's database to the currently active
        # DemoStorage (which is set by FunctionalTestCase)
        super(TestCase, self).setUp()
        db = zope.app.testing.functional.FunctionalTestSetup().db
        application = self.layer.http.application
        assert isinstance(application, zope.app.wsgi.WSGIPublisherApplication)
        factory = type(application.requestFactory)
        application.requestFactory = factory(db)
