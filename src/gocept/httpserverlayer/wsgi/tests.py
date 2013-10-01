import gocept.httpserverlayer.wsgi
import urllib

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class SimpleApp(object):

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        statuscode = '404 Not Found'
        body = 'Not Found'
        headers = []
        if path == '/':
            statuscode = '200 OK'
            headers.append(('Content-Type', 'text/html'))
            body = """
              <html>
              <head>
                <title>Test</title>
              </head>
              <body>
                <p>Hello world!</p>
              </body>
              </html>"""
        start_response(statuscode, headers)
        return body


EXAMPLE_LAYER = gocept.httpserverlayer.wsgi.Layer()
EXAMPLE_LAYER.wsgi_app = SimpleApp()


class WSGITest(unittest.TestCase):

    layer = EXAMPLE_LAYER

    def test_http_works(self):
        self.assertTrue(self.layer['httpd_thread'].isAlive)
        r = urllib.urlopen('http://%s/' % self.layer['http_address'])
        self.assertIn('Hello world', r.read())
