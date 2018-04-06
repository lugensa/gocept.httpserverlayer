import plone.testing
import plone.testing.zope


class Layer(plone.testing.Layer):
    """HTTP Server layer built using plone.testing.zope.WSGIServer."""

    host = 'localhost'
    port = 0  # choose automatically

    defaultBases = (plone.testing.zope.WSGI_SERVER_FIXTURE,
                    plone.testing.zope.FUNCTIONAL_TESTING)

    def __init__(self, *args, **kw):
        super(Layer, self).__init__(*args, **kw)
        plone.testing.zope.WSGI_SERVER_FIXTURE.host = self.host
        plone.testing.zope.WSGI_SERVER_FIXTURE.port = self.port

    def setUp(self):
        self['http_host'] = self.host
        self['http_port'] = self['port']  # set by WSGI_SERVER_FIXTURE
        self['http_address'] = '{0[http_host]}:{0[http_port]}'.format(self)

    def tearDown(self):
        del self['http_host']
        del self['http_port']
        del self['http_address']


HTTP_SERVER = Layer()
