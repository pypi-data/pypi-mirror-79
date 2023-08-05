#!/usr/bin/env python

import sys
from os import path
from setuptools import setup

if sys.version_info < (2, 7):
    raise NotImplementedError('Sorry, you need at least Python 2.7 or Python 3.4+ to use bottle.')

import bottle_json_pretty

project_dir = path.abspath(path.dirname(__file__))
with open(path.join(project_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bottle_json_pretty',
    version=bottle_json_pretty.__version__,
    description='Return pretty JSON responses from the Bottle Web Framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['bottle', 'json', 'pretty'],
    author='Jack McKernan',
    author_email='jmcker@outlook.com',
    url='https://github.com/jmcker/bottle-json-pretty',
    install_requires=['bottle'],
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Bottle',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/jmcker/bottle-json-pretty/issues',
        'Source': 'https://github.com/jmcker/bottle-json-pretty',
    },
)