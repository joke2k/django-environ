# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

from environ.compat import json


class FakeEnv:
    URL = 'http://www.google.com/'
    POSTGRES = 'postgres://uf07k1:wegauwhg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722'
    MYSQL = 'mysql://bea6eb0:69772142@us-cdbr-east.cleardb.com/heroku_97681?reconnect=true'
    MYSQLGIS = 'mysqlgis://user:password@127.0.0.1/some_database'
    SQLITE = 'sqlite:////full/path/to/your/database/file.sqlite'
    ORACLE_TNS = 'oracle://user:password@sid/'
    ORACLE = 'oracle://user:password@host:1521/sid'
    CUSTOM_BACKEND = 'custom.backend://user:password@example.com:5430/database'
    REDSHIFT = 'redshift://user:password@examplecluster.abc123xyz789.us-west-2.redshift.amazonaws.com:5439/dev'
    MEMCACHE = 'memcache://127.0.0.1:11211'
    REDIS = 'rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password=secret'
    EMAIL = 'smtps://user@domain.com:password@smtp.example.com:587'
    JSON = dict(one='bar', two=2, three=33.44)
    DICT = dict(foo='bar', test='on')
    PATH = '/home/dev'
    EXPORTED = 'exported var'

    @classmethod
    def generate_data(cls):
        return dict(STR_VAR='bar',
                    MULTILINE_STR_VAR='foo\\nbar',
                    INT_VAR='42',
                    FLOAT_VAR='33.3',
                    FLOAT_COMMA_VAR='33,3',
                    FLOAT_STRANGE_VAR1='123,420,333.3',
                    FLOAT_STRANGE_VAR2='123.420.333,3',
                    FLOAT_NEGATIVE_VAR='-1.0',
                    BOOL_TRUE_STRING_LIKE_INT='1',
                    BOOL_TRUE_INT=1,
                    BOOL_TRUE_STRING_LIKE_BOOL='True',
                    BOOL_TRUE_STRING_1='on',
                    BOOL_TRUE_STRING_2='ok',
                    BOOL_TRUE_STRING_3='yes',
                    BOOL_TRUE_STRING_4='y',
                    BOOL_TRUE_STRING_5='true',
                    BOOL_TRUE_BOOL=True,
                    BOOL_FALSE_STRING_LIKE_INT='0',
                    BOOL_FALSE_INT=0,
                    BOOL_FALSE_STRING_LIKE_BOOL='False',
                    BOOL_FALSE_BOOL=False,
                    PROXIED_VAR='$STR_VAR',
                    INT_LIST='42,33',
                    INT_TUPLE='(42,33)',
                    STR_LIST_WITH_SPACES=' foo,  bar',
                    EMPTY_LIST='',
                    DICT_VAR='foo=bar,test=on',
                    DATABASE_URL=cls.POSTGRES,
                    DATABASE_MYSQL_URL=cls.MYSQL,
                    DATABASE_MYSQL_GIS_URL=cls.MYSQLGIS,
                    DATABASE_SQLITE_URL=cls.SQLITE,
                    DATABASE_ORACLE_URL=cls.ORACLE,
                    DATABASE_ORACLE_TNS_URL=cls.ORACLE_TNS,
                    DATABASE_REDSHIFT_URL=cls.REDSHIFT,
                    DATABASE_CUSTOM_BACKEND_URL=cls.CUSTOM_BACKEND,
                    CACHE_URL=cls.MEMCACHE,
                    CACHE_REDIS=cls.REDIS,
                    EMAIL_URL=cls.EMAIL,
                    URL_VAR=cls.URL,
                    JSON_VAR=json.dumps(cls.JSON),
                    PATH_VAR=cls.PATH,
                    EXPORTED_VAR=cls.EXPORTED)
