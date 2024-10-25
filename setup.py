#!/usr/bin/env python
#
# This file is part of the django-environ.
#
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import codecs
import re
from os import path

from setuptools import find_packages, setup

# Use this code block for future deprecations of Python version:
#
# import warnings
# import sys
#
# if sys.version_info < (3, 6):
#    warnings.warn(
#        "Support of Python < 3.6 is deprecated"
#        "and will be removed in a future release.",
#        DeprecationWarning
#    )


def read_file(filepath):
    """Read content from a UTF-8 encoded text file."""
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


PKG_NAME = 'django-environ'
PKG_DIR = path.abspath(path.dirname(__file__))
META_PATH = path.join(PKG_DIR, 'environ', '__init__.py')
META_CONTENTS = read_file(META_PATH)


def load_long_description():
    """Load long description from file README.rst."""
    def changes():
        changelog = path.join(PKG_DIR, 'CHANGELOG.rst')
        pattern = (
            r'(`(v\d+.\d+.\d+)`_( - \d{1,2}-\w+-\d{4}\r?\n-+\r?\n.*?))'
            r'\r?\n\r?\n\r?\n`v\d+.\d+.\d+`_'
        )
        result = re.search(pattern, read_file(changelog), re.S)

        return result.group(2) + result.group(3) if result else ''

    try:
        title = PKG_NAME
        head = '=' * (len(title))

        contents = (
            head,
            format(title.strip(' .')),
            head,
            read_file(path.join(PKG_DIR, 'README.rst')).split(
                '.. -teaser-begin-'
            )[1],
            '',
            read_file(path.join(PKG_DIR, 'CONTRIBUTING.rst')),
            '',
            'Release Information',
            '===================\n',
            changes(),
            '',
            '`Full changelog <{}/en/latest/changelog.html>`_.'.format(
                find_meta('url')
            ),
            '',
            read_file(path.join(PKG_DIR, 'SECURITY.rst')),
            '',
            read_file(path.join(PKG_DIR, 'AUTHORS.rst')),
        )

        return '\n'.join(contents)
    except (RuntimeError, FileNotFoundError) as read_error:
        message = 'Long description could not be read from README.rst'
        raise RuntimeError('%s: %s' % (message, read_error)) from read_error


def is_canonical_version(version):
    """Check if a version string is in the canonical format of PEP 440."""
    pattern = (
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))'
        r'*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))'
        r'?(\.dev(0|[1-9][0-9]*))?$')
    return re.match(pattern, version) is not None


def find_meta(meta):
    """Extract __*meta*__ from META_CONTENTS."""
    meta_match = re.search(
        r"^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]".format(meta=meta),
        META_CONTENTS,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        'Unable to find __%s__ string in package meta file' % meta)


def get_version_string():
    """Return package version as listed in `__version__` in meta file."""
    # Parse version string
    version_string = find_meta('version')

    # Check validity
    if not is_canonical_version(version_string):
        message = (
            'The detected version string "{}" is not in canonical '
            'format as defined in PEP 440.'.format(version_string))
        raise ValueError(message)

    return version_string


# What does this project relate to?
KEYWORDS = [
    'environment',
    'django',
    'variables',
    '12factor',
]

# Classifiers: available ones listed at https://pypi.org/classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',

    'Framework :: Django',
    'Framework :: Django :: 2.2',
    'Framework :: Django :: 3.0',
    'Framework :: Django :: 3.1',
    'Framework :: Django :: 3.2',
    'Framework :: Django :: 4.0',
    'Framework :: Django :: 4.1',
    'Framework :: Django :: 4.2',
    'Framework :: Django :: 5.0',
    'Framework :: Django :: 5.1',

    'Operating System :: OS Independent',

    'Intended Audience :: Developers',
    'Natural Language :: English',

    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',

    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',

    'License :: OSI Approved :: MIT License',
]

# Dependencies that are downloaded by pip on installation and why.
INSTALL_REQUIRES = []

DEPENDENCY_LINKS = []

# List additional groups of dependencies here (e.g. testing dependencies).
# You can install these using the following syntax, for example:
#
#    $ pip install -e .[testing,docs,develop]
#
EXTRAS_REQUIRE = {
    # Dependencies that are required to run tests
    'testing': [
        'coverage[toml]>=5.0a4',  # Code coverage measurement for Python
        'pytest>=4.6.11',  # Our tests framework
        'setuptools>=71.0.0',  # Needed as a dependency for some tests
    ],
    # Dependencies that are required to build documentation
    'docs': [
        'furo>=2024.8.6',  # Sphinx documentation theme
        'sphinx>=5.0',  # Python documentation generator
        'sphinx-notfound-page',  # Create a custom 404 page
    ],
}

# Dependencies that are required to develop package
DEVELOP_REQUIRE = []

# Dependencies that are required to develop package
EXTRAS_REQUIRE['develop'] = \
    DEVELOP_REQUIRE + EXTRAS_REQUIRE['testing'] + EXTRAS_REQUIRE['docs']

# Project's URLs
PROJECT_URLS = {
    'Documentation': find_meta('url'),
    'Funding': 'https://opencollective.com/django-environ',
    'Say Thanks!': 'https://saythanks.io/to/joke2k',
    'Changelog': '{}/en/latest/changelog.html'.format(find_meta('url')),
    'Bug Tracker': 'https://github.com/joke2k/django-environ/issues',
    'Source Code': 'https://github.com/joke2k/django-environ',
}


if __name__ == '__main__':
    setup(
        name=PKG_NAME,
        version=get_version_string(),
        author=find_meta('author'),
        author_email=find_meta('author_email'),
        maintainer=find_meta('maintainer'),
        maintainer_email=find_meta('maintainer_email'),
        license=find_meta('license'),
        description=find_meta('description'),
        long_description=load_long_description(),
        long_description_content_type='text/x-rst',
        keywords=KEYWORDS,
        url=find_meta('url'),
        project_urls=PROJECT_URLS,
        classifiers=CLASSIFIERS,
        packages=find_packages(exclude=['tests.*', 'tests']),
        platforms=['any'],
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.9,<4',
        install_requires=INSTALL_REQUIRES,
        dependency_links=DEPENDENCY_LINKS,
        extras_require=EXTRAS_REQUIRE,
    )
