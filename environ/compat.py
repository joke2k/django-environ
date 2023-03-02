# This file is part of the django-environ.
#
# Copyright (c) 2021-2022, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

"""This module handles import compatibility issues."""

from pkgutil import find_loader


if find_loader('simplejson'):
    import simplejson as json
else:
    import json

if find_loader('django'):
    from django import VERSION as DJANGO_VERSION
    from django.core.exceptions import ImproperlyConfigured
else:
    DJANGO_VERSION = None

    class ImproperlyConfigured(Exception):
        """Django is somehow improperly configured"""


def choose_rediscache_driver():
    """Backward compatibility for RedisCache driver."""
    # use built-in support if Django 4+
    if DJANGO_VERSION is not None and DJANGO_VERSION >= (4, 0):
        return 'django.core.cache.backends.redis.RedisCache'

    # back compatibility with redis_cache package
    if find_loader('redis_cache'):
        return 'redis_cache.RedisCache'
    return 'django_redis.cache.RedisCache'


def choose_postgres_driver():
    """Backward compatibility for postgresql driver."""
    old_django = DJANGO_VERSION is not None and DJANGO_VERSION < (2, 0)
    if old_django:
        return 'django.db.backends.postgresql_psycopg2'
    return 'django.db.backends.postgresql'


def choose_pymemcache_driver():
    """Backward compatibility for pymemcache."""
    old_django = DJANGO_VERSION is not None and DJANGO_VERSION < (3, 2)
    if old_django or not find_loader('pymemcache'):
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
