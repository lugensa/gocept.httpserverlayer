import gocept.httpserverlayer.plonetestingzope
import gocept.httpserverlayer.plonetestingzope.testing
import gocept.httpserverlayer.tests.isolation
import unittest


class Zope2Tests(
        gocept.httpserverlayer.tests.isolation.IsolationTests,
        gocept.httpserverlayer.plonetestingzope.testing.IsolationTestHelper,
        unittest.TestCase):

    layer = gocept.httpserverlayer.plonetestingzope.testing.HTTP_LAYER
