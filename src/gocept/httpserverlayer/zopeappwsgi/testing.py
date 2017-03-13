import gocept.httpserverlayer.wsgi
import gocept.httpserverlayer.zopeappwsgi
import zope.app.appsetup.testlayer


ZODB_LAYER = zope.app.appsetup.testlayer.ZODBLayer(
    gocept.httpserverlayer.zopeappwsgi, 'testing.zcml')


class WSGILayer(gocept.httpserverlayer.zopeappwsgi.Layer):

    defaultBases = (ZODB_LAYER,)

    def get_current_zodb(self):
        return ZODB_LAYER.db


WSGI_LAYER = WSGILayer()


HTTP_LAYER = gocept.httpserverlayer.wsgi.Layer(
    name='HTTPLayer', bases=(WSGI_LAYER,))
