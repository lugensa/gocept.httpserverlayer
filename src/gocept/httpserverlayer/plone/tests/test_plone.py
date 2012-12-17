from Products.PloneTestCase.layer import PloneSiteLayer
import Products.PloneTestCase.PloneTestCase
import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zope2
import gocept.httpserverlayer.zope2.testing
import unittest


Products.PloneTestCase.PloneTestCase.setupPloneSite(id='plone')

HTTP_LAYER = gocept.httpserverlayer.zope2.Layer(
    name='HTTPLayer',
    bases=(PloneSiteLayer, gocept.httpserverlayer.zope2.testing.Layer))


class PloneTests(gocept.httpserverlayer.tests.isolation.IsolationTests,
                 gocept.httpserverlayer.plone.TestCase):

    layer = HTTP_LAYER

    def getDatabase(self):
        return gocept.httpserverlayer.zope2.testing.get_current_db()


def test_suite():
    # z2testrunner needs this
    return unittest.makeSuite(PloneTests)
