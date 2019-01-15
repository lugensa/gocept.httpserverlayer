from setuptools import setup, find_packages


setup(
    name='gocept.httpserverlayer',
    version='3.1',

    install_requires=[
        'setuptools',
        'plone.testing',
    ],

    extras_require={
        'test': [
            'shoobx.junitxml',
        ],
        'zopeappwsgi': [
            'zope.app.wsgi >= 4',
        ],
        'plonetestingzope': [
            'Zope >= 4.0b1',
            'plone.testing[zope] >= 7.0dev0',
        ],
    },

    entry_points="""
        [console_scripts]
        test = gocept.httpserverlayer.testing:test_runner
    """,

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://bitbucket.org/gocept/gocept.httpserverlayer/',

    keywords='HTTP server Plone testing zope.testrunner layer Zope',
    classifiers="""\
Development Status :: 5 - Production/Stable
Framework :: Zope :: 3
Framework :: Zope :: 4
Intended Audience :: Developers
License :: OSI Approved :: Zope Public License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
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
