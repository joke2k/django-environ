# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import pytest
from environ.environ import _cast


@pytest.mark.parametrize(
    'literal',
    ['anything-', 'anything*', '*anything', 'anything.',
     'anything.1', '(anything', 'anything-v1.2', 'anything-1.2', 'anything=']
)
def test_cast(literal):
    """Safely evaluate a string containing an invalid Python literal.

    See https://github.com/joke2k/django-environ/issues/200 for details."""
    assert _cast(literal) == literal
