import gocept.httpserverlayer.plonetesting
import gocept.httpserverlayer.plonetesting.testing
import gocept.httpserverlayer.tests.isolation
import unittest


class Zope2Tests(
    gocept.httpserverlayer.tests.isolation.IsolationTests,
    gocept.httpserverlayer.plonetesting.testing.IsolationTestHelper,
    unittest.TestCase):

    layer = gocept.httpserverlayer.plonetesting.testing.HTTP_LAYER


def test_suite():
    # z2testrunner needs this
    return unittest.makeSuite(Zope2Tests)
