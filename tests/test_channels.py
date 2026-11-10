# This file is part of the django-environ.
#
# Copyright (c) 2024-present, Daniele Faraglia <daniele.faraglia@gmail.com>
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

from environ import Env
import pytest
from django.core.exceptions import ImproperlyConfigured


def test_channels_parsing():
    url = "inmemory://"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels.layers.InMemoryChannelLayer"

    url = "redis://user:password@localhost:6379/0"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels_redis.core.RedisChannelLayer"
    assert result["CONFIG"]["hosts"][0] == "redis://user:password@localhost:6379/0"

    url = "rediss://user:password@localhost:6379/0"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels_redis.core.RedisChannelLayer"
    assert result["CONFIG"]["hosts"][0] == "rediss://user:password@localhost:6379/0"

    url = "redis+pubsub://user:password@localhost:6379/0"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels_redis.pubsub.RedisPubSubChannelLayer"
    assert result["CONFIG"]["hosts"][0] == "redis://user:password@localhost:6379/0"

    url = "rediss+pubsub://user:password@localhost:6379/0"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels_redis.pubsub.RedisPubSubChannelLayer"
    assert result["CONFIG"]["hosts"][0] == "rediss://user:password@localhost:6379/0"

@pytest.mark.parametrize('url', [
    'unsupported://',
    'redis+custom://redis.example.invalid:6379/4',
    'valkey://redis.example.invalid:6379/4',
    'inmemory://',
])
def test_channels_backend_override(url):
    result = Env.channels_url_config(url, backend='custom.backend')
    assert result == {'BACKEND': 'custom.backend'}


@pytest.mark.parametrize('backend_override', [None, 'custom.backend'])
@pytest.mark.parametrize('url,host,default_backend', [
    ('redis://redis.example.invalid:6380/4?socket_timeout=2',
     'redis://redis.example.invalid:6380/4?socket_timeout=2',
     'channels_redis.core.RedisChannelLayer'),
    ('rediss://redis.example.invalid:6380/4?socket_timeout=2',
     'rediss://redis.example.invalid:6380/4?socket_timeout=2',
     'channels_redis.core.RedisChannelLayer'),
    ('redis+pubsub://redis.example.invalid:6380/4?socket_timeout=2',
     'redis://redis.example.invalid:6380/4?socket_timeout=2',
     'channels_redis.pubsub.RedisPubSubChannelLayer'),
    ('rediss+pubsub://redis.example.invalid:6380/4?socket_timeout=2',
     'rediss://redis.example.invalid:6380/4?socket_timeout=2',
     'channels_redis.pubsub.RedisPubSubChannelLayer'),
])
def test_channels_backend_override_preserves_hosts(
        monkeypatch, url, host, default_backend, backend_override):
    backend = backend_override or default_backend
    monkeypatch.setenv('CHANNELS_URL', url)

    result = Env().channels_url(backend=backend)

    assert result['BACKEND'] == backend
    assert result.get('CONFIG', {}).get('hosts') == [host]


def test_channels_invalid_schema():
    with pytest.raises(ImproperlyConfigured) as exc:
        Env.channels_url_config("unsupported://")
    assert 'Invalid channels schema unsupported' == str(exc.value)
