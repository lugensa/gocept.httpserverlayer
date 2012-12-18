import gocept.httpserverlayer.plonetesting
import gocept.httpserverlayer.plonetesting.testing_plone
import gocept.httpserverlayer.tests.isolation
import unittest


class PloneTests(
    gocept.httpserverlayer.tests.isolation.IsolationTests,
    gocept.httpserverlayer.plonetesting.testing.IsolationTestHelper,
    unittest.TestCase):

    layer = gocept.httpserverlayer.plonetesting.testing_plone.HTTP_LAYER
