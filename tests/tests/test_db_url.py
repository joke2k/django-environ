# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev, <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

from environ import Env
from environ.compat import DJANGO_POSTGRES


def test_db_url_config():
    cfg = Env.db_url_config('sqlite://:memory:')
    assert len(cfg) == 2
    assert cfg['ENGINE'] == 'django.db.backends.sqlite3'
    assert cfg['NAME'] == ':memory:'

    cfg = Env.db_url_config('sqlite:////full/path/to/your/file.sqlite')
    assert len(cfg) == 6
    assert cfg['ENGINE'] == 'django.db.backends.sqlite3'
    assert cfg['NAME'] == '/full/path/to/your/file.sqlite'
    for k in ['HOST', 'PASSWORD', 'PORT', 'USER']:
        assert cfg[k] == ''

    cfg = Env.db_url_config(
        ('postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@'
         'ec2-107-21-253-135.compute-1.amazonaws.com:5431/'
         'd8r82722r2kuvn')
    )
    assert len(cfg) == 6
    assert cfg['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
    assert cfg['NAME'] == 'd8r82722r2kuvn'
    assert cfg['PASSWORD'] == 'wegauwhgeuioweg'
    assert cfg['PORT'] == 5431
    assert cfg['USER'] == 'uf07k1i6d8ia0v'
    assert cfg['ENGINE'] == DJANGO_POSTGRES
