#!/usr/bin/env python3

from distutils.core import setup
import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kblab-client',
    version='0.0.16a0',
    description='KB lab client',
    author='Martin Malmsten',
    author_email='martin.malmsten@kb.se',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kungbib/kblab",
    install_requires = [
        'requests',
        'pyyaml',
        'lxml',
        'htfile'
    ],
    packages=[ 'kblab' ],
    include_package_data = True
)

