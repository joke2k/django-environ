# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import warnings

import pytest

from environ import Env
from environ.compat import DJANGO_POSTGRES


@pytest.mark.parametrize(
    'url,engine,name,host,user,passwd,port',
    [
        ('postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.'
         'compute-1.amazonaws.com:5431/d8r82722r2kuvn',
         DJANGO_POSTGRES,
         'd8r82722r2kuvn',
         'ec2-107-21-253-135.compute-1.amazonaws.com',
         'uf07k1i6d8ia0v',
         'wegauwhgeuioweg',
         5431),
        ('postgres:////var/run/postgresql/db',
         DJANGO_POSTGRES,
         'db',
         '/var/run/postgresql',
         '',
         '',
         ''),
        ('postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.'
         'compute-1.amazonaws.com:5431/d8r82722r2kuvn',
         'django.contrib.gis.db.backends.postgis',
         'd8r82722r2kuvn',
         'ec2-107-21-253-135.compute-1.amazonaws.com',
         'uf07k1i6d8ia0v',
         'wegauwhgeuioweg',
         5431),
        ('mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.'
         'compute-1.amazonaws.com:5431/d8r82722r2kuvn',
         'django.contrib.gis.db.backends.mysql',
         'd8r82722r2kuvn',
         'ec2-107-21-253-135.compute-1.amazonaws.com',
         'uf07k1i6d8ia0v',
         'wegauwhgeuioweg',
         5431),
        ('mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com'
         '/heroku_97681db3eff7580?reconnect=true',
         'django.db.backends.mysql',
         'heroku_97681db3eff7580',
         'us-cdbr-east.cleardb.com',
         'bea6eb025ca0d8',
         '69772142',
         ''),
        ('mysql://travis@localhost/test_db',
         'django.db.backends.mysql',
         'test_db',
         'localhost',
         'travis',
         '',
         ''),
        ('sqlite://',
         'django.db.backends.sqlite3',
         ':memory:',
         '',
         '',
         '',
         ''),
        ('sqlite:////full/path/to/your/file.sqlite',
         'django.db.backends.sqlite3',
         '/full/path/to/your/file.sqlite',
         '',
         '',
         '',
         ''),
        ('sqlite://:memory:',
         'django.db.backends.sqlite3',
         ':memory:',
         '',
         '',
         '',
         ''),
        ('ldap://cn=admin,dc=nodomain,dc=org:'
         'some_secret_password@ldap.nodomain.org/',
         'ldapdb.backends.ldap',
         'ldap://ldap.nodomain.org',
         'ldap.nodomain.org',
         'cn=admin,dc=nodomain,dc=org',
         'some_secret_password',
         ''),
    ],
    ids=[
        'postgres',
        'postgres_unix_domain',
        'postgis',
        'mysqlgis',
        'cleardb',
        'mysql_no_password',
        'sqlite_empty',
        'sqlite_file',
        'sqlite_memory',
        'ldap',
    ],
)
def test_db_parsing(url, engine, name, host, user, passwd, port):
    config = Env.db_url_config(url)

    assert config['ENGINE'] == engine
    assert config['NAME'] == name

    if url != 'sqlite://:memory:':
        assert config['PORT'] == port
        assert config['PASSWORD'] == passwd
        assert config['USER'] == user
        assert config['HOST'] == host


def test_postgres_complex_db_name_parsing():
    """Make sure we can use complex postgres host."""
    env_url = (
        'postgres://user:password@//cloudsql/'
        'project-1234:us-central1:instance/dbname'
    )

    url = Env.db_url_config(env_url)

    assert url['ENGINE'] == DJANGO_POSTGRES
    assert url['HOST'] == '/cloudsql/project-1234:us-central1:instance'
    assert url['NAME'] == 'dbname'
    assert url['USER'] == 'user'
    assert url['PASSWORD'] == 'password'
    assert url['PORT'] == ''


@pytest.mark.parametrize(
    'scheme',
    ['postgres', 'postgresql', 'psql', 'pgsql', 'postgis'],
)
def test_postgres_like_scheme_parsing(scheme):
    """Verify all the postgres-like schemes parsed the same as postgres."""
    env_url1 = (
        'postgres://user:password@//cloudsql/'
        'project-1234:us-central1:instance/dbname'
    )
    env_url2 = (
        '{}://user:password@//cloudsql/'
        'project-1234:us-central1:instance/dbname'
    ).format(scheme)

    url1 = Env.db_url_config(env_url1)
    url2 = Env.db_url_config(env_url2)

    assert url2['NAME'] == url1['NAME']
    assert url2['PORT'] == url1['PORT']
    assert url2['PASSWORD'] == url1['PASSWORD']
    assert url2['USER'] == url1['USER']
    assert url2['HOST'] == url1['HOST']

    if scheme == 'postgis':
        assert url2['ENGINE'] == 'django.contrib.gis.db.backends.postgis'
    else:
        assert url2['ENGINE'] == url1['ENGINE']


def test_memory_sqlite_url_warns_about_netloc(recwarn):
    warnings.simplefilter("always")

    url = 'sqlite://missing-slash-path'
    url = Env.db_url_config(url)

    assert len(recwarn) == 1
    assert recwarn.pop(UserWarning)

    assert url['ENGINE'] == 'django.db.backends.sqlite3'
    assert url['NAME'] == ':memory:'


def test_database_options_parsing():
    url = 'postgres://user:pass@host:1234/dbname?conn_max_age=600'
    url = Env.db_url_config(url)
    assert url['CONN_MAX_AGE'] == 600

    url = ('postgres://user:pass@host:1234/dbname?'
           'conn_max_age=None&autocommit=True&atomic_requests=False')
    url = Env.db_url_config(url)
    assert url['CONN_MAX_AGE'] is None
    assert url['AUTOCOMMIT'] is True
    assert url['ATOMIC_REQUESTS'] is False

    url = ('mysql://user:pass@host:1234/dbname?init_command=SET '
           'storage_engine=INNODB')
    url = Env.db_url_config(url)
    assert url['OPTIONS'] == {
        'init_command': 'SET storage_engine=INNODB',
    }
