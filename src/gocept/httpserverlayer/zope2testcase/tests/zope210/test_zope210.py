import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zope2testcase
import gocept.httpserverlayer.zope2testcase.testing
import unittest


class Zope2Tests(gocept.httpserverlayer.tests.isolation.IsolationTests,
                 gocept.httpserverlayer.zope2testcase.TestCase):

    layer = gocept.httpserverlayer.zope2testcase.testing.HTTP_LAYER

    def getDatabase(self):
        return gocept.httpserverlayer.zope2testcase.testing.get_current_db()


def test_suite():
    # z2testrunner needs this
    return unittest.makeSuite(Zope2Tests)
