"""
Heavily based upon Django's setup.py that seems to automate things nicely.
"""
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import os
import sys

def fullsplit(path, result=None):
    """
    Split pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
flow_dir = 'flow'

for dirpath, dirnames, filenames in os.walk(flow_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Dynamically calculate the version based on flow.VERSION.
version = __import__('flow').get_version()

setup(
    name='flow',
    author='Fluidinfo Inc',
    author_email='dev@fluidinfo.com',
    version=version,
    requires=['fom', 'flimp', 'jinja2'],
    url='http://fluidinfo.com/',
    description='A small framework for writing self-hosted (web) applications for FluidDB',
    long_description=open('README.rst').read(),
    packages = packages,
    data_files = data_files,
    scripts=['bin/flow'],
    classifiers=['Development Status :: 3 - Alpha Development Status',
                 'Environment :: Web Environment',
                 'Framework :: FluidDB',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python, Javascript, HTML',
                 'Topic :: Utilities',
                 'Topic :: Software Development :: Libraries :: Application Frameworks',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Internet :: WWW/HTTP',
                 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                 ]
)
