from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='gocept.httpserverlayer',
    version='2.0',

    install_requires=[
        'setuptools',
        'plone.testing',
    ],

    extras_require={
        'zopeappwsgi': [
            'zope.app.wsgi',
        ],
        'plonetestingz2': [
            'plone.testing[z2]',
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
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('', glob.glob(project_path('*.txt')))],
    zip_safe=False,
)
