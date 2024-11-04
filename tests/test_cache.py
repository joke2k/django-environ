# This file is part of the django-environ.
#
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

from unittest import mock

import pytest

import environ.compat
from environ import Env
from environ.compat import (
    ImproperlyConfigured,
    PYMEMCACHE_DRIVER,
    REDIS_DRIVER,
)


def test_base_options_parsing():
    url = ('memcache://127.0.0.1:11211/?timeout=0&'
           'key_prefix=cache_&key_function=foo.get_key&version=1')
    url = Env.cache_url_config(url)

    assert url['KEY_PREFIX'] == 'cache_'
    assert url['KEY_FUNCTION'] == 'foo.get_key'
    assert url['TIMEOUT'] == 0
    assert url['VERSION'] == 1

    url = 'redis://127.0.0.1:6379/?timeout=None'
    url = Env.cache_url_config(url)

    assert url['TIMEOUT'] is None


@pytest.mark.parametrize(
    'url,backend,location',
    [
        ('dbcache://my_cache_table',
         'django.core.cache.backends.db.DatabaseCache', 'my_cache_table'),
        ('filecache:///var/tmp/django_cache',
         'django.core.cache.backends.filebased.FileBasedCache',
         '/var/tmp/django_cache'),
        ('filecache://C:/foo/bar',
         'django.core.cache.backends.filebased.FileBasedCache', 'C:/foo/bar'),
        ('locmemcache://',
         'django.core.cache.backends.locmem.LocMemCache', ''),
        ('locmemcache://unique-snowflake',
         'django.core.cache.backends.locmem.LocMemCache', 'unique-snowflake'),
        ('dummycache://',
         'django.core.cache.backends.dummy.DummyCache', ''),
        ('rediss://127.0.0.1:6379/1', REDIS_DRIVER,
         'rediss://127.0.0.1:6379/1'),
        ('rediscache://:redispass@127.0.0.1:6379/0', REDIS_DRIVER,
         'redis://:redispass@127.0.0.1:6379/0'),
        ('rediscache://host1:6379,host2:6379,host3:9999/1', REDIS_DRIVER,
         ['redis://host1:6379/1', 'redis://host2:6379/1',
          'redis://host3:9999/1']),
        ('rediscache:///path/to/socket:1', REDIS_DRIVER,
         'unix:///path/to/socket:1'),
        ('memcache:///tmp/memcached.sock',
         'django.core.cache.backends.memcached.MemcachedCache',
         'unix:/tmp/memcached.sock'),
        ('memcache://172.19.26.240:11211,172.19.26.242:11212',
         'django.core.cache.backends.memcached.MemcachedCache',
         ['172.19.26.240:11211', '172.19.26.242:11212']),
        ('memcache://127.0.0.1:11211',
         'django.core.cache.backends.memcached.MemcachedCache',
         '127.0.0.1:11211'),
        ('pymemcache://127.0.0.1:11211',
         PYMEMCACHE_DRIVER,
         '127.0.0.1:11211'),
        ('pymemcache://memcached:11211/?key_prefix=ci',
         PYMEMCACHE_DRIVER,
         'memcached:11211'),
    ],
    ids=[
        'dbcache',
        'filecache',
        'filecache_win',
        'locmemcache_empty',
        'locmemcache',
        'dummycache',
        'rediss',
        'redis_with_password',
        'redis_multiple',
        'redis_socket',
        'memcached_socket',
        'memcached_multiple',
        'memcached',
        'pylibmccache',
        'pylibmccache_trailing_slash',
    ],
)
def test_cache_parsing(url, backend, location):
    url = Env.cache_url_config(url)

    assert url['BACKEND'] == backend
    assert url['LOCATION'] == location


@pytest.mark.parametrize('django_version', ((3, 2), (3, 1), None))
@pytest.mark.parametrize('pymemcache_installed', (True, False))
def test_pymemcache_compat(django_version, pymemcache_installed):
    old = 'django.core.cache.backends.memcached.PyLibMCCache'
    new = 'django.core.cache.backends.memcached.PyMemcacheCache'
    with mock.patch.object(environ.compat, 'DJANGO_VERSION', django_version):
        with mock.patch('environ.compat.find_spec') as mock_find_spec:
            mock_find_spec.return_value = pymemcache_installed
            driver = environ.compat.choose_pymemcache_driver()
            if django_version and django_version < (3, 2):
                assert driver == old
            else:
                assert driver == new if pymemcache_installed else old


@pytest.mark.parametrize('django_version', ((4, 0), (3, 2), None))
@pytest.mark.parametrize('django_redis_installed', (True, False))
def test_rediscache_compat(django_version, django_redis_installed):
    django_new = 'django.core.cache.backends.redis.RedisCache'
    redis_cache = 'redis_cache.RedisCache'
    django_redis = 'django_redis.cache.RedisCache'

    with mock.patch.object(environ.compat, 'DJANGO_VERSION', django_version):
        with mock.patch('environ.compat.find_spec') as mock_find_spec:
            mock_find_spec.return_value = django_redis_installed
            driver = environ.compat.choose_rediscache_driver()
            if django_redis_installed:
                assert driver == django_redis
            elif django_version and django_version >= (4, 0):
                assert driver == django_new
            else:
                assert driver == redis_cache

def test_redis_parsing():
    url = ('rediscache://127.0.0.1:6379/1?client_class='
           'django_redis.client.DefaultClient&password=secret')
    url = Env.cache_url_config(url)

    assert url['BACKEND'] == REDIS_DRIVER
    assert url['LOCATION'] == 'redis://127.0.0.1:6379/1'
    assert url['OPTIONS'] == {
        'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        'PASSWORD': 'secret',
    }


def test_redis_socket_url():
    url = 'redis://:redispass@/path/to/socket.sock?db=0'
    url = Env.cache_url_config(url)
    assert REDIS_DRIVER == url['BACKEND']
    assert url['LOCATION'] == 'unix://:redispass@/path/to/socket.sock'
    assert url['OPTIONS'] == {
        'DB': 0
    }


def test_options_parsing():
    url = 'filecache:///var/tmp/django_cache?timeout=60&max_entries=1000&cull_frequency=0'
    url = Env.cache_url_config(url)

    assert url['BACKEND'] == 'django.core.cache.backends.filebased.FileBasedCache'
    assert url['LOCATION'] == '/var/tmp/django_cache'
    assert url['TIMEOUT'] == 60
    assert url['OPTIONS'] == {
        'MAX_ENTRIES': 1000,
        'CULL_FREQUENCY': 0,
    }


def test_custom_backend():
    url = 'memcache://127.0.0.1:5400?foo=option&bars=9001'
    backend = 'django_redis.cache.RedisCache'
    url = Env.cache_url_config(url, backend)

    assert url['BACKEND'] == backend
    assert url['LOCATION'] == '127.0.0.1:5400'
    assert url['OPTIONS'] == {
        'FOO': 'option',
        'BARS': 9001,
    }


def test_unknown_backend():
    url = 'unknown-scheme://127.0.0.1:1000'
    with pytest.raises(ImproperlyConfigured) as excinfo:
        Env.cache_url_config(url)
    assert str(excinfo.value) == 'Invalid cache schema unknown-scheme'


def test_empty_url_is_mapped_to_empty_config():
    assert Env.cache_url_config('') == {}
    assert Env.cache_url_config(None) == {}


@pytest.mark.parametrize(
    'chars',
    ['!', '$', '&', "'", '(', ')', '*', '+', ';', '=', '-', '.', '-v1.2']
)
def test_cache_url_password_using_sub_delims(monkeypatch, chars):
    """Ensure CACHE_URL passwords may contains some unsafe characters.

    See: https://github.com/joke2k/django-environ/issues/200 for details."""
    url = 'rediss://enigma:secret{}@ondigitalocean.com:25061/2'.format(chars)
    monkeypatch.setenv('CACHE_URL', url)
    env = Env()

    result = env.cache()
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url

    result = env.cache_url_config(url)
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url

    url = 'rediss://enigma:sec{}ret@ondigitalocean.com:25061/2'.format(chars)
    monkeypatch.setenv('CACHE_URL', url)
    env = Env()

    result = env.cache()
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url

    result = env.cache_url_config(url)
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url

    url = 'rediss://enigma:{}secret@ondigitalocean.com:25061/2'.format(chars)
    monkeypatch.setenv('CACHE_URL', url)
    env = Env()

    result = env.cache()
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url

    result = env.cache_url_config(url)
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url


@pytest.mark.parametrize(
    'chars', ['%3A', '%2F', '%3F', '%23', '%5B', '%5D', '%40', '%2C']
)
def test_cache_url_password_using_gen_delims(monkeypatch, chars):
    """Ensure CACHE_URL passwords may contains %-encoded characters.

    See: https://github.com/joke2k/django-environ/issues/200 for details."""
    url = 'rediss://enigma:secret{}@ondigitalocean.com:25061/2'.format(chars)
    monkeypatch.setenv('CACHE_URL', url)
    env = Env()

    result = env.cache()
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url

    url = 'rediss://enigma:sec{}ret@ondigitalocean.com:25061/2'.format(chars)
    monkeypatch.setenv('CACHE_URL', url)
    env = Env()

    result = env.cache()
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url

    url = 'rediss://enigma:{}secret@ondigitalocean.com:25061/2'.format(chars)
    monkeypatch.setenv('CACHE_URL', url)
    env = Env()

    result = env.cache()
    assert result['BACKEND'] == REDIS_DRIVER
    assert result['LOCATION'] == url


def test_cache_url_env_using_default():
    env = Env(CACHE_URL=(str, "locmemcache://"))
    result = env.cache()

    assert result["BACKEND"] == "django.core.cache.backends.locmem.LocMemCache"
    assert result["LOCATION"] == ""
