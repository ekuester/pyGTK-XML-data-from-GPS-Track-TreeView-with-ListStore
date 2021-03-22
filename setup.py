#!/usr/bin/env python3
from setuptools import find_packages, setup

with open('VERSION') as f:
    VERSION=f.read()

setup(name='pyXMLGPX-parser.py',
    version=VERSION,
    description='Read XML data from a GPX file und display the GPS trackpoints in a table',
    url='https://github.com/ekuester/pyGTK-XML-data-from-GPS-Track-TreeView-with-ListStore',
    author='Erich Küster',
    author_email='erich.kuester@arcor.de',
    license='MIT',
    package_data={
        # include files found in the "pyXMLGPX-parser" package
        'pyXMLGPX-parser': ['*.xpm', 'COMMENTS', 'LICENSE', 'locale/*/LC_MESSAGES/*.mo'],
    },
    package_include=[True],
    packages=['pyXMLGPX-parser'],
    zip_safe=False)

