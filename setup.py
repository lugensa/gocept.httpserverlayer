from setuptools import setup, find_packages


setup(
    name='gocept.httpserverlayer',
    version='2.3.dev0',

    install_requires=[
        'setuptools',
        'plone.testing',
    ],

    extras_require={
        'zopeappwsgi': [
            'zope.app.wsgi',
        ],
        'plonetestingz2': [
            'transaction < 2.0',
            'ZODB < 5.0',
            'plone.testing[z2] < 5.1',
        ],
        'plonetestingz4': [
            'ZServer >= 4.0a1',
            'plone.testing[z2] >= 5.1.1',
        ],
    },

    entry_points={
    },

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://bitbucket.org/gocept/gocept.httpserverlayer/',

    keywords='HTTP Plone testing zope.testrunner layer Zope',
    classifiers="""\
Development Status :: 5 - Production/Stable
Framework :: Zope :: 2
Framework :: Zope :: 3
Framework :: Zope :: 4
Intended Audience :: Developers
License :: OSI Approved :: Zope Public License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: Implementation :: CPython
Topic :: Internet :: WWW/HTTP :: HTTP Servers
Topic :: Software Development :: Testing
"""[:-1].split('\n'),
    description='HTTP server integration for testing',
    long_description='\n\n'.join(open(name).read() for name in (
        'README.rst',
        'HACKING.rst',
        'CHANGES.rst',
    )),

    namespace_packages=['gocept'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
