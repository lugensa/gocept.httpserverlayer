import gocept.httpserverlayer.static
import os
import unittest
import urllib2


class TestStaticFiles(unittest.TestCase):

    def setUp(self):
        self.testlayer = gocept.httpserverlayer.static.STATIC_FILES
        self.testlayer.setUp()

    def tearDown(self):
        self.testlayer.tearDown()

    def test_documentroot_is_in_a_tempdir(self):
        import tempfile
        self.assertTrue(self.testlayer['documentroot'].startswith(
            tempfile.tempdir))

    def test_documentroot_initially_empty(self):
        documentroot = self.testlayer['documentroot']
        self.assertEqual([], os.listdir(self.testlayer['documentroot']))
        open(os.path.join(documentroot, 'foo.txt'), 'w').write('Hello World!')
        self.assertEqual(
            ['foo.txt'], os.listdir(self.testlayer['documentroot']))

    def test_documentroot_empty_except_for_favicon_after_testsetup(self):
        documentroot = self.testlayer['documentroot']
        self.assertEqual([], os.listdir(self.testlayer['documentroot']))
        open(os.path.join(documentroot, 'bar.txt'), 'w').write('Hello World!')
        self.assertEqual(
            ['bar.txt'], os.listdir(self.testlayer['documentroot']))
        self.testlayer.testSetUp()
        self.assertEqual(
            ['favicon.ico'], os.listdir(self.testlayer['documentroot']))

    def test_serves_files(self):
        open(os.path.join(self.testlayer['documentroot'], 'foo.txt'), 'w')\
            .write('Hello World!')
        response = urllib2.urlopen(
            'http://%s/foo.txt' % self.testlayer['http_address'])
        self.assertEqual('Hello World!', response.read())


class TestStaticFilesShutdown(unittest.TestCase):

    def test_server_startup_shutdown(self):
        layer = gocept.httpserverlayer.static.STATIC_FILES
        layer.setUp()
        self.assertTrue(layer['httpd_thread'].isAlive())
        layer.tearDown()
        self.assertFalse(layer.get('httpd'))


class TestStaticLayerInAction(unittest.TestCase):

    layer = gocept.httpserverlayer.static.STATIC_FILES

    def test_should_return_files(self):
        open(os.path.join(self.layer['documentroot'], 'index'), 'w')\
        .write('Hello World!')
        r = urllib2.urlopen('http://%s/index' % self.layer['http_address'])
        self.assertTrue('Hello World' in r.read())
