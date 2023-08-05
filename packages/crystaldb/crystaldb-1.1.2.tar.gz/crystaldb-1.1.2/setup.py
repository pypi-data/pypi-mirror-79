# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Zhichang Fu
# Created Time: 2018-10-06 12:33:04

from setuptools import setup
import os

try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
    readme = f.read()
    f.close()
except Exception:
    readme = "CrystalDB is a simple and small ORM and  no need to provide a model."

install_requires = ["mysqlclient", "DBUtils"]
_version = "1.1.2"

setup(
    name='crystaldb',
    description=
    'CrystalDB is a simple and small ORM and  no need to provide a model.',
    long_description=readme,
    author='Zhichang Fu',
    author_email='fuzctc@gmail.com',
    long_description_content_type="text/markdown",
    url='https://github.com/fuzctc/crystaldb.py.git',
    version=_version,
    packages=['crystaldb'],
    requires=install_requires,
    install_requires=install_requires,
    include_package_data=True,
    exclude_package_date={'': ['.gitignore']}
)
