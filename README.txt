======================
gocept.httpserverlayer
======================

This package provides an HTTP server for testing your application with normal
HTTP clients (e.g. a real browser). This is done using `test layers`_, which
are a feature of `zope.testrunner`_.

gocept.httpserverlayer uses `plone.testing`_ for the test layer implementation,
and exposes the following resources (accessible in your test case as
``self.layer[RESOURCE_NAME]``):

:http_host: The hostname of the HTTP server (Default: localhost)
:http_port: The port of the HTTP server (Default: 0, which means chosen
            automatically by the operating system)
:http_address: ``hostname:port``, convenient to use in URLs
   (e.g. ``'http://user:password@%s/path' % self.layer['http_address']``)

This package is compatible with Python versions 2.6 - 2.7.

.. _`test layers`: http://pypi.python.org/pypi/plone.testing#layers
.. _`zope.testrunner`: http://pypi.python.org/pypi/zope.testrunner
.. _`plone.testing`: http://pypi.python.org/pypi/plone.testing

.. contents::


WSGI
====

This test layer takes a WSGI callable and runs it in a temporary HTTP server::

    import gocept.httpserverlayer.wsgi
    from mypackage import App
    import unittest

    HTTP_LAYER = gocept.httpserverlayer.wsgi.Layer()
    HTTP_LAYER.wsgi_app = App()

    class WSGIExample(unittest.TestCase):

        layer = HTTP_LAYER

        def test_something(self):
            r = urllib.urlopen('http://%s/' % self.layer['http_address'])
            self.assertIn('Hello world', r.read())

You can also have a base layer provide the WSGI callable (in the
``wsgi_app`` resource)::


    import gocept.httpserverlayer.wsgi
    from mypackage import App
    import plone.testing

    class WSGILayer(plone.testing.Layer):

        def setUp(self):
            self['wsgi_app'] = App()

    WSGI_LAYER = WSGILayer()

    HTTP_LAYER = gocept.httpserverlayer.wsgi.Layer(
        name='HTTPLayer', bases=(WSGI_LAYER,))


Static files
============

This test layer serves up the contents of a directory::

    import gocept.httpserverlayer.static
    import pkg_resources
    import unittest

    HTTP_LAYER = gocept.httpserverlayer.static.Layer(
        pkg_resources.resource_filename('my.package.tests', 'fixtures'))

    class DirecoryExample(unittest.TestCase):

        layer = HTTP_LAYER

        def test_something(self):
            r = urllib.urlopen('http://%s/index' % self.layer['http_address'])
            self.assertIn('Hello world', r.read())

If you don't pass in a directory, a temporary directory will be created/removed
automatically. The directory is provided in the ``documentroot`` resource.
For convenience, a layer instance is already provided as ``STATIC_FILES``::

    import gocept.httpserverlayer.static
    import os.path
    import unittest

    HTTP_LAYER = gocept.httpserverlayer.static.STATIC_FILES

    class TemporaryExample(unittest.TestCase):

        layer = HTTP_LAYER

        def test_something(self):
            open(os.path.join(self.testlayer['documentroot'], 'index'), 'w')\
            .write('Hello World!')
            r = urllib.urlopen('http://%s/index' % self.layer['http_address'])
            self.assertIn('Hello world', r.read())


Custom request handler
======================

This test layer allows you to provide your own HTTP request handler for very
fine-grained control::

    import gocept.httpserverlayer.custom
    import unittest

    class RequestHandler(gocept.httpserverlayer.custom.RequestHandler):

        response_code = 200
        response_body = ''
        posts_received = []

        def do_POST(self):
            length = int(self.headers['content-length'])
            self.posts_received.append(dict(
                path=self.path,
                data=self.rfile.read(length),
                headers=self.headers,
            ))
            self.send_response(self.response_code)
            self.end_headers()
            self.wfile.write(self.response_body)

    HTTP_LAYER = gocept.httpserverlayer.custom.Layer(RequestHandler)

    class POSTExample(unittest.TestCase):

        layer = HTTP_LAYER

        def test_something(self):
            urllib.urlopen('http://%s/' % self.layer['http_address'],
                urllib.urlencode({'foo': 'bar'}))
            self.assertEqual(
                'foo=bar', self.layer['request_handler'].posts_received[0]['data'])


Framework integration
=====================

gocept.httpserverlayer also provides integration with several web frameworks.
Different frameworks require different dependencies; this is handled via
setuptools extras of gocept.httpserverlayer (e.g. for Grok integration you need
to require ``gocept.httpserverlayer[zopeappwsgi]``).

Most flavours require the usage of a specialised ``TestCase`` in addition to
the test layer.


Zope3 / ZTK (zope.app.testing)
==============================

Requires ``gocept.httpserverlayer[zopeapptesting]``.

This test layer builds on the usual ZCMLLayer that is used for typical ZTK
functional tests::

    import gocept.httpserverlayer.zopeapptesting
    import zope.app.testing.functional

    ZCML_LAYER = zope.app.testing.functional.ZCMLLayer(
        'ftesting.zcml', __name__, __name__, allow_teardown=True)
    HTTP_LAYER = gocept.httpserverlayer.zopeapptesting.Layer(
        name='HTTPLayer', bases=(ZCML_LAYER,))

    class ZTKExample(gocept.httpserverlayer.zopeapptesting.TestCase):

        layer = HTTP_LAYER

        def test(self):
            r = urllib.urlopen('http://%s/' % self.layer['http_address'])
            self.assertIn('Hello world', r.read())


Zope3 / ZTK / Grok (zope.app.wsgi)
==================================

Requires ``gocept.httpserverlayer[zopeappwsgi]``

If your ZTK application uses ``zope.app.wsgi.testlayer`` (which is the
recommended test setup for Grok, for example), you can use
``gocept.httpserverlayer.zopeappwsgi.Layer`` to create a WSGI app that
integrates ZODB isolation, and ``gocept.httpserverlayer.wsgi.Layer`` to provide
the actual HTTP server. No special TestCase is required, ``unittest.TestCase``
is enough.

The ``zopeappwsgi.Layer`` expects to find the current ZODB in the plone.testing
resource ``zodbDB`` (which is used by ``plone.testing.zodb.EMPTY_ZODB``), or
you can inherit and override ``get_current_zodb``. Here's an example setup for
Grok (which uses ``zope.app.appsetup.testlayer.ZODBLayer``)::

    import gocept.httpserverlayer.wsgi
    import gocept.httpserverlayer.zopeappwsgi
    import unittest
    import zope.app.appsetup.testlayer

    ZODB_LAYER = zope.app.appsetup.testlayer.ZODBLayer(
        gocept.httpserverlayer.zopeappwsgi, 'testing.zcml')

    class WSGILayer(gocept.httpserverlayer.zopeappwsgi.Layer):

        defaultBases = (ZODB_LAYER,)

        def get_current_zodb(self):
            return ZODB_LAYER.db

    WSGI_LAYER = WSGILayer()

    HTTP_LAYER = gocept.httpserverlayer.wsgi.Layer(
        name='HTTPLayer', bases=(WSGI_LAYER,))

    class GrokExample(unittest.TestCase):

        layer = HTTP_LAYER

        def test(self):
            r = urllib.urlopen('http://%s/' % self.layer['http_address'])
            self.assertIn('Hello world', r.read())


Zope 2 via WSGI
===============

If your Zope 2 setup supports it, you can use the WSGI integration instead of a
specialised Zope 2 integration to run your tests.

You might see the following exception when running tests::

    File ".../repoze.retry-1.0-py2.7.egg/repoze/retry/__init__.py", line 55, in __call__
      cl = int(cl)
     ValueError: invalid literal for int() with base 10: ''

To fix this issue you can use an additional middleware around your WSGI
application: ``gocept.httpserverlayer.wsgi.FixupMiddleware``.


Plone (ZopeTestCase)
====================

Requires ``gocept.httpserverlayer[plonetestcase]``.

This test layer builds on ``Products.PloneTestCase.laye.PloneSiteLayer``::

    from Products.PloneTestCase.layer import PloneSiteLayer
    import Products.PloneTestCase.PloneTestCase
    import gocept.httpserverlayer.plone

    Products.PloneTestCase.PloneTestCase.setupPloneSite(id='plone')

    HTTP_LAYER = gocept.httpserverlayer.zope2.Layer(
        name='HTTPLayer', bases=(PloneSiteLayer,))

    class PloneTests(gocept.httpserverlayer.plone.TestCase):

        layer = HTTP_LAYER

        def test(self):
            r = urllib.urlopen('http://%s/' % self.layer['http_address'])
            self.assertIn('Hello world', r.read())


Zope 2 / Plone (plone.testing.z2)
=================================

Requires ``gocept.httpserverlayer[plonetestingz2]``.

gocept.httpserverlayer provides a ``plone.testing.Layer`` at
``gocept.httpserverlayer.plonetesting.HTTP_SERVER`` that you can mix and match
with your base layers. No special TestCase is required, ``unittest.TestCase``
is enough.

For a plain Zope2 application this might look like this (uses
``plone.testing[z2]``)::

    import gocept.httpserverlayer.plonetesting
    import plone.testing
    import plone.testing.z2

    class Layer(plone.testing.Layer):

        defaultBases = (plone.testing.z2.STARTUP,)

        def setUp(self):
            zope.configuration.xmlconfig.file(
                'testing.zcml', package=mypackage,
                context=self['configurationContext'])

    Z2_LAYER = Layer()

    HTTP_LAYER = plone.testing.Layer(
        name='HTTPLayer',
        bases=(Z2_LAYER, gocept.httpserverlayer.plonetesting.HTTP_SERVER))

And for a Plone application like this (uses ``plone.app.testing``)::

    import gocept.httpserverlayer.plonetesting
    import plone.app.testing.layers
    import plone.testing

    HTTP_LAYER = plone.testing.Layer(
        name='HTTPLayer',
        bases=(plone.app.testing.layers.PLONE_FIXTURE,
               gocept.httpserverlayer.plonetesting.HTTP_SERVER))
