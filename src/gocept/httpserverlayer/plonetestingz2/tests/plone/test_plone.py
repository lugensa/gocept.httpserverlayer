import gocept.httpserverlayer.plonetestingz2
import gocept.httpserverlayer.plonetestingz2.testing_plone
import gocept.httpserverlayer.tests.isolation
import unittest


class PloneTests(
    gocept.httpserverlayer.tests.isolation.IsolationTests,
    gocept.httpserverlayer.plonetestingz2.testing.IsolationTestHelper,
    unittest.TestCase):

    layer = gocept.httpserverlayer.plonetestingz2.testing_plone.HTTP_LAYER
