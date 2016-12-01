from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='gocept.httpserverlayer',
    version='2.1',

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
            'plone.testing[z2]',
        ],
        'plonetestingz4': [
            'ZODB < 5.0',
            'transaction < 2.0',
            'ZServer >= 4.0a1',
            'plone.testing[z2] > 5.0',
        ],
    },

    entry_points={
    },

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://bitbucket.org/gocept/gocept.httpserverlayer/',

    keywords='',
    classifiers="""\
License :: OSI Approved :: Zope Public License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 2 :: Only
"""[:-1].split('\n'),
    description='HTTP server integration for testing',
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
        'README.rst',
        'HACKING.rst',
        'CHANGES.rst',
    )),

    namespace_packages=['gocept'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('',
                 glob.glob(project_path('*.txt')),
                 glob.glob(project_path('*.rst')))],
    zip_safe=False,
)
