import gocept.httpserverlayer.plonetestingzope
import plone.testing
import plone.testing.zope
import zope.configuration.xmlconfig


class Layer(plone.testing.Layer):

    defaultBases = (plone.testing.zope.STARTUP,)

    def setUp(self):
        zope.configuration.xmlconfig.file(
            'testing.zcml', package=gocept.httpserverlayer.plonetestingzope,
            context=self['configurationContext'])


ZOPE_LAYER = Layer()


HTTP_LAYER = plone.testing.Layer(
    name='HTTPLayer',
    bases=(ZOPE_LAYER, gocept.httpserverlayer.plonetestingzope.HTTP_SERVER))


class IsolationTestHelper(object):
    """
    plone.testing implementation of methods needed by common isolation tests
    """

    def getDatabase(self):
        return self.layer['zodbDB']

    def getRootFolder(self):
        return self.layer['app']
