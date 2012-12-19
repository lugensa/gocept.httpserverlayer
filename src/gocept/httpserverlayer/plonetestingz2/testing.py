import gocept.httpserverlayer.plonetestingz2
import plone.testing
import plone.testing.z2
import zope.configuration.xmlconfig


class Layer(plone.testing.Layer):

    defaultBases = (plone.testing.z2.STARTUP,)

    def setUp(self):
        zope.configuration.xmlconfig.file(
            'testing.zcml', package=gocept.httpserverlayer.plonetestingz2,
            context=self['configurationContext'])


Z2_LAYER = Layer()


HTTP_LAYER = plone.testing.Layer(
    name='HTTPLayer',
    bases=(Z2_LAYER, gocept.httpserverlayer.plonetestingz2.HTTP_SERVER))


class IsolationTestHelper(object):
    """
    plone.testing implementation of methods needed by common isolation tests
    """

    def getDatabase(self):
        return self.layer['zodbDB']

    def getRootFolder(self):
        return self.layer['app']
