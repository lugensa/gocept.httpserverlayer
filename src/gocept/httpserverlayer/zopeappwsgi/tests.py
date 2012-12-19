import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zopeappwsgi.testing
import unittest


class GrokTests(gocept.httpserverlayer.tests.isolation.IsolationTests,
                unittest.TestCase):

    layer = gocept.httpserverlayer.zopeappwsgi.testing.HTTP_LAYER

    def getDatabase(self):
        return gocept.httpserverlayer.zopeappwsgi.testing.ZODB_LAYER.db

    def getRootFolder(self):
        return gocept.httpserverlayer.zopeappwsgi.testing.ZODB_LAYER.getRootFolder()
