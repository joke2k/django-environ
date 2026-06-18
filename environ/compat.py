# This file is part of the django-environ.
#
# Copyright (c) 2024-present, Daniele Faraglia <daniele.faraglia@gmail.com>
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

"""This module handles import compatibility issues."""

from importlib.util import find_spec

import django


def choose_rediscache_driver():
    """Backward compatibility for RedisCache driver."""

    # django-redis library takes precedence
    if find_spec('django_redis'):
        return 'django_redis.cache.RedisCache'

    # use built-in support if Django 4+
    if django.VERSION >= (4, 0):
        return 'django.core.cache.backends.redis.RedisCache'

    # back compatibility with redis_cache package
    return 'redis_cache.RedisCache'


def choose_postgres_driver():
    """Backward compatibility for postgresql driver."""
    return 'django.db.backends.postgresql'


def choose_pymemcache_driver():
    """Backward compatibility for pymemcache."""
    old_django = django.VERSION < (3, 2)
    if old_django or not find_spec('pymemcache'):
        # The original backend choice for the 'pymemcache' scheme is
        # unfortunately 'pylibmc'.
        return 'django.core.cache.backends.memcached.PyLibMCCache'
    return 'django.core.cache.backends.memcached.PyMemcacheCache'


REDIS_DRIVER = choose_rediscache_driver()
"""The name of the RedisCache driver."""

DJANGO_POSTGRES = choose_postgres_driver()
"""The name of the PostgreSQL driver."""

PYMEMCACHE_DRIVER = choose_pymemcache_driver()
"""The name of the Pymemcache driver."""
