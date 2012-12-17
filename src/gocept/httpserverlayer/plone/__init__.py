import Products.PloneTestCase.PloneTestCase
import gocept.httpserverlayer.zope2


class TestCase(gocept.httpserverlayer.zope2.SandboxPatch,
               Products.PloneTestCase.PloneTestCase.FunctionalTestCase):

    def getRootFolder(self):
        """forward API-compatibility with zope.app.testing"""
        return self.app
