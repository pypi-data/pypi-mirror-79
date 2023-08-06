#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
 name = 'lstmx',
 version = '0.0.3',
 description = 'library ',
 long_description = 'library ',
 author = 'ligaopan',
 author_email = 'ligaopan1984@163.com',
 url = 'https://github.com/ligaopan/lgp-library',
 license = 'MIT Licence',
 keywords = 'testing testautomation',
 platforms = 'any',
 python_requires = '>=3.7.*',
 install_requires = [],
 package_dir = {'': 'src'},
 packages = find_packages('src')
 )