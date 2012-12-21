from Products.PloneTestCase.layer import PloneSiteLayer
import Products.PloneTestCase.PloneTestCase
import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zope2testcase
import gocept.httpserverlayer.zope2testcase.testing
import unittest


Products.PloneTestCase.PloneTestCase.setupPloneSite(id='plone')

HTTP_LAYER = gocept.httpserverlayer.zope2testcase.Layer(
    name='HTTPLayer',
    bases=(PloneSiteLayer,
           gocept.httpserverlayer.zope2testcase.testing.ZCML_LAYER))


class PloneTests(gocept.httpserverlayer.tests.isolation.IsolationTests,
                 gocept.httpserverlayer.plonetestcase.TestCase):

    layer = HTTP_LAYER

    def getDatabase(self):
        return gocept.httpserverlayer.zope2testcase.testing.get_current_db()


def test_suite():
    # z2testrunner needs this
    return unittest.makeSuite(PloneTests)
