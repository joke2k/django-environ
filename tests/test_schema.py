# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import os

from environ import Env
from .fixtures import FakeEnv

_old_environ = None


def setup_module():
    """Setup environment variables to the execution for the current module."""
    global _old_environ

    _old_environ = os.environ
    os.environ = Env.ENVIRON = FakeEnv.generate_data()


def teardown_module():
    """Restore environment variables was previously setup in setup_module."""
    global _old_environ

    assert _old_environ is not None
    os.environ = _old_environ


def test_schema():
    env = Env(INT_VAR=int, NOT_PRESENT_VAR=(float, 33.3), STR_VAR=str,
              INT_LIST=[int], DEFAULT_LIST=([int], [2]))

    assert isinstance(env('INT_VAR'), int)
    assert env('INT_VAR') == 42

    assert isinstance(env('NOT_PRESENT_VAR'), float)
    assert env('NOT_PRESENT_VAR') == 33.3

    assert 'bar' == env('STR_VAR')
    assert 'foo' == env('NOT_PRESENT2', default='foo')

    assert isinstance(env('INT_LIST'), list)
    assert env('INT_LIST') == [42, 33]

    assert isinstance(env('DEFAULT_LIST'), list)
    assert env('DEFAULT_LIST') == [2]

    # Override schema in this one case
    assert isinstance(env('INT_VAR', cast=str), str)
    assert env('INT_VAR', cast=str) == '42'
