# This file is part of the django-environ.
#
# Copyright (c) 2021-2022, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import pytest

from environ.environ import _cast, _cast_urlstr


@pytest.mark.parametrize(
    'literal',
    ['anything-', 'anything*', '*anything', 'anything.',
     'anything.1', '(anything', 'anything-v1.2', 'anything-1.2', 'anything=']
)
def test_cast(literal):
    """Safely evaluate a string containing an invalid Python literal.

    See https://github.com/joke2k/django-environ/issues/200 for details."""
    assert _cast(literal) == literal


@pytest.mark.parametrize(
    "quoted_url_str,expected_unquoted_str",
    [
        ("Le-%7BFsIaYnaQw%7Da2B%2F%5BV8bS+", "Le-{FsIaYnaQw}a2B/[V8bS+"),
        ("my_test-string+", "my_test-string+"),
        ("my%20test%20string+", "my test string+")
    ]
)
def test_cast_urlstr(quoted_url_str, expected_unquoted_str):
    """Make sure that a url str that contains plus sign literals does not get unquoted incorrectly
    Plus signs should not be converted to spaces, since spaces are encoded with %20 in URIs

    see https://github.com/joke2k/django-environ/issues/357 for details.
    related to https://github.com/joke2k/django-environ/pull/69"""

    assert _cast_urlstr(quoted_url_str) == expected_unquoted_str
