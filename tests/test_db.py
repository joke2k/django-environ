# This file is part of the django-environ.
#
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
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
        # postgres://user:password@host:port/dbname
        ('postgres://enigma:secret@example.com:5431/dbname',
         DJANGO_POSTGRES,
         'dbname',
         'example.com',
         'enigma',
         'secret',
         5431),
        # postgres://path/dbname
        ('postgres:////var/run/postgresql/dbname',
         DJANGO_POSTGRES,
         'dbname',
         '/var/run/postgresql',
         '',
         '',
         ''),
        # postgis://user:password@host:port/dbname
        ('postgis://enigma:secret@example.com:5431/dbname',
         'django.contrib.gis.db.backends.postgis',
         'dbname',
         'example.com',
         'enigma',
         'secret',
         5431),
        # postgres://user:password@host:port,host:port,host:port/dbname
        ('postgres://username:p@ss:12,wor:34d@host1:111,22.55.44.88:222,[2001:db8::1234]:333/db',
         DJANGO_POSTGRES,
         'db',
         'host1,22.55.44.88,[2001:db8::1234]',
         'username',
         'p@ss:12,wor:34d',
         '111,222,333'
         ),
        # postgres://host,host,host/dbname
        ('postgres://node1,node2,node3/db',
         DJANGO_POSTGRES,
         'db',
         'node1,node2,node3',
         '',
         '',
         ''
         ),
        # cockroachdb://username:secret@test.example.com:26258/dbname
        ('cockroachdb://username:secret@test.example.com:26258/dbname',
         'django_cockroachdb',
         'dbname',
         'test.example.com',
         'username',
         'secret',
         26258),
        # mysqlgis://user:password@host:port/dbname
        ('mysqlgis://enigma:secret@example.com:5431/dbname',
         'django.contrib.gis.db.backends.mysql',
         'dbname',
         'example.com',
         'enigma',
         'secret',
         5431),
        # mysql://user:password@host/dbname?options
        ('mysql://enigma:secret@reconnect.com/dbname?reconnect=true',
         'django.db.backends.mysql',
         'dbname',
         'reconnect.com',
         'enigma',
         'secret',
         ''),
        # mysql://user@host/dbname
        ('mysql://enigma@localhost/dbname',
         'django.db.backends.mysql',
         'dbname',
         'localhost',
         'enigma',
         '',
         ''),
        # sqlite://
        ('sqlite://',
         'django.db.backends.sqlite3',
         ':memory:',
         '',
         '',
         '',
         ''),
        # sqlite:////absolute/path/to/db/file
        ('sqlite:////full/path/to/your/file.sqlite',
         'django.db.backends.sqlite3',
         '/full/path/to/your/file.sqlite',
         '',
         '',
         '',
         ''),
        # sqlite://:memory:
        ('sqlite://:memory:',
         'django.db.backends.sqlite3',
         ':memory:',
         '',
         '',
         '',
         ''),
        # ldap://user:password@host
        ('ldap://cn=admin,dc=nodomain,dc=org:secret@example.com',
         'ldapdb.backends.ldap',
         'ldap://example.com',
         'example.com',
         'cn=admin,dc=nodomain,dc=org',
         'secret',
         ''),
        # mysql://user:password@host/dbname
        ('mssql://enigma:secret@example.com/dbname'
         '?driver=ODBC Driver 13 for SQL Server',
         'mssql',
         'dbname',
         'example.com',
         'enigma',
         'secret',
         ''),
        # mysql://user:password@host:port/dbname
        ('mssql://enigma:secret@amazonaws.com\\insnsnss:12345/dbname'
         '?driver=ODBC Driver 13 for SQL Server',
         'mssql',
         'dbname',
         'amazonaws.com\\insnsnss',
         'enigma',
         'secret',
         12345),
         # mysql://user:password@host:port/dbname
        ('mysql://enigma:><{~!@#$%^&*}[]@example.com:1234/dbname',
         'django.db.backends.mysql',
         'dbname',
         'example.com',
         'enigma',
         '><{~!@#$%^&*}[]',
         1234),
        # mysql://user:password@host/dbname
        ('mysql://enigma:]password]@example.com/dbname',
         'django.db.backends.mysql',
         'dbname',
         'example.com',
         'enigma',
         ']password]',
         ''),
    ],
    ids=[
        'postgres',
        'postgres_unix_domain',
        'postgis',
        'postgres_cluster',
        'postgres_no_ports',
        'cockroachdb',
        'mysqlgis',
        'cleardb',
        'mysql_no_password',
        'sqlite_empty',
        'sqlite_file',
        'sqlite_memory',
        'ldap',
        'mssql',
        'mssql_port',
        'mysql_password_special_chars',
        'mysql_invalid_ipv6_password',
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

    if engine == 'sql_server.pyodbc':
        assert config['OPTIONS'] == {'driver': 'ODBC Driver 13 for SQL Server'}

    if host == 'reconnect.com':
        assert config['OPTIONS'] == {'reconnect': 'true'}


def test_custom_db_engine():
    """Override ENGINE determined from schema."""
    env_url = 'postgres://enigma:secret@example.com:5431/dbname'

    engine = 'mypackage.backends.whatever'
    url = Env.db_url_config(env_url, engine=engine)

    assert url['ENGINE'] == engine


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
