import plone.testing
import plone.testing.z2


# XXX it would be nicer to reuse plone.testing.z2.ZSERVER_FIXTURE,
# but we can't, since we want to be able to override host/port
ZSERVER = plone.testing.z2.ZServer()


class Layer(plone.testing.Layer):

    host = 'localhost'
    port = 0  # choose automatically

    defaultBases = (ZSERVER, plone.testing.z2.FUNCTIONAL_TESTING)

    def __init__(self, *args, **kw):
        super(Layer, self).__init__(*args, **kw)
        ZSERVER.host = self.host
        ZSERVER.port = self.port

    def setUp(self):
        _, self.port = ZSERVER.zserver.socket.getsockname()
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)

    def tearDown(self):
        del self['http_host']
        del self['http_port']
        del self['http_address']


HTTP_SERVER = Layer()
