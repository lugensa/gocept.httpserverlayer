import gocept.httpserverlayer.tests.isolation
import gocept.httpserverlayer.zopeapptesting.testing
import zope.app.testing.functional


class ZTKTests(gocept.httpserverlayer.tests.isolation.IsolationTests,
               gocept.httpserverlayer.zopeapptesting.testing.TestCase):

    def getDatabase(self):
        return zope.app.testing.functional.FunctionalTestSetup().db
