# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

from environ import Env


def test_channels_parsing():
    url = "inmemory://"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels.layers.InMemoryChannelLayer"

    url = "redis://user:password@localhost:5173/0"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels_redis.core.RedisChannelLayer"
    assert result["CONFIG"]["hosts"][0] == "redis://user:password@localhost:5173/0"

    url = "redis+pubsub://user:password@localhost:5173/0"
    result = Env.channels_url_config(url)
    assert result["BACKEND"] == "channels_redis.pubsub.RedisPubSubChannelLayer"
    assert result["CONFIG"]["hosts"][0] == "redis://user:password@localhost:5173/0"
