import gocept.httpserverlayer.plonetestingz2
import gocept.httpserverlayer.plonetestingz2.testing
import gocept.httpserverlayer.tests.isolation
import unittest


class Zope2Tests(
        gocept.httpserverlayer.tests.isolation.IsolationTests,
        gocept.httpserverlayer.plonetestingz2.testing.IsolationTestHelper,
        unittest.TestCase):

    layer = gocept.httpserverlayer.plonetestingz2.testing.HTTP_LAYER
