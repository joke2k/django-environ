#!/usr/bin/env python

import os

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'django-environ'
PACKAGE = 'environ'
DESCRIPTION = "Django-environ allows you to utilize 12factor inspired environment " \
              "variables to configure your Django application."
URL = 'https://github.com/joke2k/django-environ'
EMAIL = 'daniele.faraglia@gmail.com'
AUTHOR = 'joke2k'
VERSION = '0.6.0'
LICENSE = 'MIT'

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
LONG_DESCRIPTION = '\n' + open(os.path.join(here, 'README.rst'), encoding="utf8").read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    keywords='django environment variables 12factor',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    platforms=["any"],
    python_requires=">=3",
    include_package_data=True,
    test_suite='environ.test.load_suite',
    zip_safe=False,
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django'
    ]
)
