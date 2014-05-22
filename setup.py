from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='gocept.httpserverlayer',
    version='1.5.2',

    install_requires=[
        'setuptools',
        'plone.testing',
    ],

    extras_require={
        'test': [
        ],
        'zopeapptesting': [
            'zope.app.server',
            'zope.app.testing',
            'zope.app.wsgi',
            'zope.server',
        ],
        'test_zopeapptesting': [
            'zope.app.appsetup',
            'zope.app.zcmlfiles',
            'zope.securitypolicy',
            'zope.testing >= 3.8.0',
            'zope.interface',
            'zope.schema',
            'ZODB3',
        ],
        'zopeappwsgi': [
            'zope.app.wsgi',
        ],
        'test_zopeappwsgi': [
            'grok',
            'zope.app.appsetup',
            'ZODB3',
        ],
        'zope2testcase': [
            'Zope2',  # Zope2>=2.12 is eggified
        ],
        'plonetestcase': [
            'Products.PloneTestCase',
        ],
        'test_plonetestcase': [
            'Plone',
            'PILwoTK',
        ],
        'plonetestingz2': [
            'plone.testing[z2]',
        ],
        'test_plonetestingz2': [
            'Plone',
            'PILwoTK',
            'plone.app.testing',
        ],
    },

    entry_points={
    },

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://projects.gocept.com/projects/gocept-httpserverlayer/',

    keywords='',
    classifiers="""\
License :: OSI Approved :: Zope Public License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 2 :: Only
"""[:-1].split('\n'),
    description='HTTP server integration for testing',
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
        'README.txt',
        'HACKING.txt',
        'CHANGES.txt',
    )),

    namespace_packages=['gocept'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('', glob.glob(project_path('*.txt')))],
    zip_safe=False,
)
