=====================================
Change log for gocept.httpserverlayer
=====================================


3.1 (2019-01-15)
================

- Create a wheel of the package.

- Add support for Python 3.7.


3.0 (2018-06-29)
================

- Add support for Python 3.6.

- Drop support for Zope 2.x

- Rename the setup.py extra `plonetestingz2` into `plonetestingzope`.

- Rename the module `.plonetestingz2` into `.plonetestingzope`.


2.2 (2016-12-02)
================

- Ensure compatibility with `setuptools >= 30.0`.


2.1 (2016-12-01)
================

- Support the upcoming Zope 4 through extras_require [plonetestingz4].

- Pin `transaction < 2.0` and `ZODB < 5.0` until `Zope2` is compatible with
  these releases. (See https://github.com/zopefoundation/Zope/issues/79)


2.0 (2016-04-12)
================

- Drop support for:

  - ``zope.app.testing`` (extras_require: [zopeapptesting])

  - ``Testing.ZopeTestCase`` (extras_require: [zope2testcase])

  - ``plone.app.testing`` (extras_require: [test_plonetestingz2])

  - ``Products.PloneTestCase`` (extras_require: [plonetestcase])

- Drop support for Python 2.6.

- Use ``tox`` as testrunner.

- Remove ``zc.buildout`` infrastructure.


1.5.3 (2015-01-09)
==================

- Don't overwrite ``self.port`` when it was 0.


1.5.2 (2014-05-22)
==================

- Silence "error 32: Broken pipe" errors in ``custom.Layer``, too.


1.5.1 (2014-02-10)
==================

- Silence "error 32: Broken pipe" errors in ``wsgi.Layer``, they just
  mean the client closed the connection prematurely, which is as
  harmless as it is normal.


1.5.0 (2013-11-07)
==================

- Make it possible to dictate the hostname for the httpserver via environment
  variable ``GOCEPT_HTTP_APP_HOST``. You will need this if you run your tests
  in a selenium grid on different machines.


1.4.1 (2013-10-01)
==================

- 1.4.0 was a brown-bag, let's try again.


1.4.0 (2013-10-01)
==================

- Make HTTP server and thread objects used by layers available as a resource.


1.3.0 (2013-07-18)
==================

- Replace dependency on ``distribute`` with ``setuptools``, since the projects have merged.


1.2.1 (2013-02-07)
==================

- Fix custom layer test tear down.


1.2 (2013-02-06)
================

- Fixed tests run on MacOS.

- Use the `server_address` instead of `server_name` of `HTTPServer` to be
  compatible with MacOS.

- Dropped compatability with Zope < 2.12.

- Removed customized `HTTPServer`, the `BaseHTTPServer.HTTPServer` does
  everything we need.


1.1 (2013-02-03)
================

- Add ``custom.Layer`` that uses a BaseHTTPServer with a custom RequestHandler,
  and ``static.Layer`` that server the contents of a directory.

- Dropped compatability with Python < 2.6.


1.0.1 (2012-12-21)
==================

- Avoid the property.setter spelling in the wsgi layer's code for Python 2.5
  compatibility.

- Conditionally require wsgiref to make the wsgi layer work with Python 2.4.

- Fixed an import in the plonetestcase layer's tests.


1.0 (2012-12-19)
================

initial release (extracted from gocept.selenium-1.0)
