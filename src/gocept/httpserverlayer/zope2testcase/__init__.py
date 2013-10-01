import Lifetime
import Testing.ZopeTestCase
import Testing.ZopeTestCase.ZopeLite
import Testing.ZopeTestCase.threadutils
import Testing.ZopeTestCase.utils
import ZServer.HTTPServer
import Zope2
import asyncore
import plone.testing
import time


class Layer(plone.testing.Layer):

    host = 'localhost'
    port = 0  # choose automatically

    def setUp(self):
        # adapted from Testing.ZopeTestCase.utils.startZServer() to make
        # host/port configurable
        Testing.ZopeTestCase.threadutils.setNumberOfThreads(1)
        log = None
        thread = Testing.ZopeTestCase.threadutils.QuietThread(
            target=Testing.ZopeTestCase.threadutils.zserverRunner,
            args=(self.host, self.port, log))
        thread.setDaemon(True)
        thread.start()
        self.port = self._find_bound_port()
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)
        # notify ZopeTestCase infrastructure that a ZServer has been started
        Testing.ZopeTestCase.utils._Z2HOST = self.host
        Testing.ZopeTestCase.utils._Z2PORT = self.port

    def _find_bound_port(self):
        for i in range(1000):
            time.sleep(0.025)
            for dispatcher in asyncore.socket_map.values():
                if isinstance(dispatcher, ZServer.HTTPServer.zhttp_server):
                    try:
                        return dispatcher.server_port
                    except AttributeError:
                        # Seems to happen when the dispatcher instance has been
                        # created, but the port wasn't bound, yet. Just ignore
                        # and wait for the next cycle.
                        pass

    def tearDown(self):
        Lifetime.shutdown(0, fast=1)
        del self['http_host']
        del self['http_port']
        del self['http_address']


class SandboxPatch(object):
    # Testing.ZopeTestCase.sandbox.Sandbox swapping of the DemoStorage is a
    # little... crude:
    #
    # ZApplicationWrapper is instantiated with a DB from
    # Testing/custom_zodb, which is never used later on, since Sandbox
    # passes in the connection (to the current DB) to use instead. This
    # connection is also stored globally in
    # Testing.ZopeTestCase.sandbox.AppZapper (and passed to requests via
    # the bobo_traverse monkey-patch there) -- which means that there only
    # ever is one single ZODB connection, among the test code and the HTTP
    # requests, and among concurrent requests. This clearly is not what we
    # want.
    #
    # Thus, this rewrite of the upstream method, that properly changes the
    # DB in ZApplicationWrapper and does *not* use AppZapper, yielding a
    # new connection upon each traversal. (For reference and since it took
    # me quite a while to figure out where everything is: this code is
    # adapted from the original Sandbox._app and the normal Zope2 startup
    # in Zope2.__init__).

    def _app(self):
        Zope2.startup()
        stuff = Zope2.bobo_application._stuff
        db = Testing.ZopeTestCase.ZopeLite.sandbox()
        Zope2.bobo_application._stuff = (db,) + stuff[1:]
        app = Zope2.bobo_application()
        app = Testing.ZopeTestCase.utils.makerequest(app)
        Testing.ZopeTestCase.connections.register(app)
        return app


class TestCase(SandboxPatch, Testing.ZopeTestCase.FunctionalTestCase):

    def getRootFolder(self):
        """forward API-compatibility with zope.app.testing"""
        return self.app
