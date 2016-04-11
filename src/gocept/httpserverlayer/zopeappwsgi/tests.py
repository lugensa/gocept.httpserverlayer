import gocept.httpserverlayer.tests.isolation
from gocept.httpserverlayer.zopeappwsgi.testing import ZODB_LAYER
import unittest


class GrokTests(gocept.httpserverlayer.tests.isolation.IsolationTests,
                unittest.TestCase):

    layer = gocept.httpserverlayer.zopeappwsgi.testing.HTTP_LAYER

    def getDatabase(self):
        return ZODB_LAYER.db

    def getRootFolder(self):
        return ZODB_LAYER.getRootFolder()
