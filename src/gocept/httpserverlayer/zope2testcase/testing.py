import Products.Five.zcml
import Testing.ZopeTestCase
import Zope2
import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zope2testcase
import plone.testing


try:
    import Testing.ZopeTestCase.layer
    bases = (Testing.ZopeTestCase.layer.ZopeLiteLayer,)
except ImportError:
    bases = ()


class ZCMLLayer(plone.testing.Layer):

    defaultBases = bases

    def setUp(self):
        Testing.ZopeTestCase.installProduct('Five')
        Products.Five.zcml.load_config(
            'configure.zcml', package=Products.Five)
        Products.Five.zcml.load_config(
            'configure.zcml', package=gocept.httpserverlayer.tests.isolation)

ZCML_LAYER = ZCMLLayer()

HTTP_LAYER = gocept.httpserverlayer.zope2testcase.Layer(
    name='HTTPLayer', bases=(ZCML_LAYER,))


def get_current_db():
    """helper for gocept.httpserverlayer.tests.isolation"""
    return Zope2.bobo_application._stuff[0]
