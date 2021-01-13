from http.server import SimpleHTTPRequestHandler
from urllib.parse import unquote
import gocept.httpserverlayer.custom
import os
import os.path
import posixpath
import shutil
import tempfile


class StaticFileRequestHandler(
        gocept.httpserverlayer.custom.RequestHandler,
        SimpleHTTPRequestHandler):

    # The documentroot is set on the class just before passing the class on
    # to the BaseHTTPServer.HTTPServer.
    documentroot = None

    def translate_path(self, path):
        # We subclass SimpleHTTPRequestHandler as it is dependent on
        # the cwd. We however want to inject a different path as the
        # "documentroot".
        # The rest of the method's implementation is copied verbatim from
        # SimpleHTTPServer.SimpleHTTPRequestHandler.
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(unquote(path))
        words = path.split('/')
        words = filter(None, words)

        path = self.documentroot
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    # Add conditional logging to handler.
    def log_request(self, *args):
        if 'GOCEPT_HTTP_VERBOSE_LOGGING' in os.environ:
            SimpleHTTPRequestHandler.log_request(self, *args)


TEMPORARY = object()


class Layer(gocept.httpserverlayer.custom.Layer):

    def __init__(self, documentroot=TEMPORARY, *args, **kw):
        super().__init__(StaticFileRequestHandler, *args, **kw)
        self.documentroot = documentroot

    def setUp(self):
        documentroot = self.documentroot
        if documentroot is TEMPORARY:
            documentroot = tempfile.mkdtemp(
                suffix='gocept.httpserverlayer.static')
        self['documentroot'] = documentroot
        self.request_handler.documentroot = self['documentroot']
        super().setUp()

    def tearDown(self):
        super().tearDown()
        if self.documentroot is TEMPORARY:
            shutil.rmtree(self['documentroot'])
        del self['documentroot']

    def testSetUp(self):
        super().testSetUp()
        paths = os.listdir(self['documentroot'])
        for path in paths:
            fullpath = os.path.join(self['documentroot'], path)
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
                continue
            os.remove(fullpath)
        # silence annoying 404s
        open(os.path.join(self['documentroot'], 'favicon.ico'), 'w').close()


STATIC_FILES = Layer()
