#!/usr/bin/env python
"""
Setup helpers for django-environ package.
Extracted from old_setup.py to generate combined README.
"""

import codecs
import re
from os import path


def read_file(filepath):
    """Read content from a UTF-8 encoded text file."""
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


def find_meta(meta):
    """Extract __*meta*__ from environ/__init__.py."""
    PKG_DIR = path.abspath(path.dirname(__file__))
    META_PATH = path.join(PKG_DIR, 'environ', '__init__.py')
    META_CONTENTS = read_file(META_PATH)

    meta_match = re.search(
        r"^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]".format(meta=meta),
        META_CONTENTS,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        'Unable to find __%s__ string in package meta file' % meta)


def load_long_description():
    """Load long description from file README.rst. Copied from old_setup.py."""
    PKG_DIR = path.abspath(path.dirname(__file__))
    PKG_NAME = 'django-environ'

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


# Generate the combined README file when imported during build
PKG_DIR = path.abspath(path.dirname(__file__))
combined_path = path.join(PKG_DIR, 'README_COMBINED.rst')

try:
    long_description = load_long_description()
    with codecs.open(combined_path, 'w', 'utf-8') as f:
        f.write(long_description)
except Exception:
    # Fallback to basic README if generation fails
    import shutil
    shutil.copy('README.rst', combined_path)