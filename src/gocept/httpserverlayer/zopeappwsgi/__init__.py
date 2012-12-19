import plone.testing
import zope.app.wsgi


class Layer(plone.testing.Layer):

    def setUp(self):
        # since the request factory class is only a parameter default of
        # WSGIPublisherApplication and not easily accessible otherwise, we fake
        # it into creating a requestFactory instance, so we can read the class
        # off of that in testSetUp()
        fake_db = object()
        self['wsgi_app'] = zope.app.wsgi.WSGIPublisherApplication(fake_db)

    def testSetUp(self):
        # tell the publisher to use ZODBLayer's current database
        factory = type(self['wsgi_app'].requestFactory)
        self['wsgi_app'].requestFactory = factory(self.get_current_zodb())

    def get_current_zodb(self):
        return self['zodbDB']
