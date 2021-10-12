# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
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
        pass

# back compatibility with django postgresql package
if DJANGO_VERSION is not None and DJANGO_VERSION < (2, 0):
    DJANGO_POSTGRES = 'django.db.backends.postgresql_psycopg2'
else:
    # https://docs.djangoproject.com/en/2.0/releases/2.0/#id1
    DJANGO_POSTGRES = 'django.db.backends.postgresql'

# back compatibility with redis_cache package
if find_loader('redis_cache'):
    REDIS_DRIVER = 'redis_cache.RedisCache'
else:
    REDIS_DRIVER = 'django_redis.cache.RedisCache'


# back compatibility for pymemcache
def choose_pymemcache_driver():
    old_django = DJANGO_VERSION is not None and DJANGO_VERSION < (3, 2)
    if old_django or not find_loader('pymemcache'):
        # The original backend choice for the 'pymemcache' scheme is
        # unfortunately 'pylibmc'.
        return 'django.core.cache.backends.memcached.PyLibMCCache'
    return 'django.core.cache.backends.memcached.PyMemcacheCache'


PYMEMCACHE_DRIVER = choose_pymemcache_driver()
