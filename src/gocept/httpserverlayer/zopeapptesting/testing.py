import gocept.httpserverlayer.zopeapptesting
import pkg_resources
import zope.app.testing.functional


ZCML_LAYER = zope.app.testing.functional.ZCMLLayer(
    pkg_resources.resource_filename(
        'gocept.httpserverlayer.zopeapptesting', 'testing.zcml'),
    __name__, 'zcml_layer', allow_teardown=True)


HTTP_LAYER = gocept.httpserverlayer.zopeapptesting.Layer(
    name='HTTPLayer', bases=(ZCML_LAYER,))


class TestCase(gocept.httpserverlayer.zopeapptesting.TestCase):

    layer = HTTP_LAYER
