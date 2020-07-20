"""
environ.compat
~~~~~~~~~~~~~~~
This module handles import compatibility issues
"""

import pkgutil


if pkgutil.find_loader('simplejson'):
    import simplejson as json
else:
    import json

if pkgutil.find_loader('django'):
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
if pkgutil.find_loader('redis_cache'):
    REDIS_DRIVER = 'redis_cache.RedisCache'
else:
    REDIS_DRIVER = 'django_redis.cache.RedisCache'
