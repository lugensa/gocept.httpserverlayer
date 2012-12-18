import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zope2
import gocept.httpserverlayer.zope2.testing
import unittest


class Zope2Tests(gocept.httpserverlayer.tests.isolation.IsolationTests,
                 gocept.httpserverlayer.zope2.TestCase):

    layer = gocept.httpserverlayer.zope2.testing.HTTP_LAYER

    def getDatabase(self):
        return gocept.httpserverlayer.zope2.testing.get_current_db()


def test_suite():
    # z2testrunner needs this
    return unittest.makeSuite(Zope2Tests)
