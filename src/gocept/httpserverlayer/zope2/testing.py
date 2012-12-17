import Products.Five.zcml
import Zope2
import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zope2


class Layer(object):

    @classmethod
    def setUp(cls):
        Products.Five.zcml.load_config(
            'configure.zcml', package=gocept.httpserverlayer.tests.isolation)


class FiveLayer(object):

    @classmethod
    def setUp(cls):
        Products.Five.zcml.load_config(
            'configure.zcml', package=Products.Five)

try:
    import Testing.ZopeTestCase.layer
    HTTP_LAYER = gocept.httpserverlayer.zope2.Layer(
        name='HTTPLayer212',
        bases=(Testing.ZopeTestCase.layer.ZopeLiteLayer, FiveLayer, Layer))
except ImportError:
    HTTP_LAYER = gocept.httpserverlayer.zope2.Layer(
        name='HTTPLayer210', bases=(Layer,))


def get_current_db():
    """helper for gocept.httpserverlayer.tests.isolation"""
    return Zope2.bobo_application._stuff[0]
