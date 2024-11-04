# This file is part of the django-environ.
#
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import os
import tempfile
from urllib.parse import quote

import pytest

from environ import Env, Path
from environ.compat import (
    DJANGO_POSTGRES,
    ImproperlyConfigured,
    REDIS_DRIVER,
)
from .asserts import assert_type_and_value
from .fixtures import FakeEnv


@pytest.mark.parametrize(
        'variable,value,raw_value,parse_comments',
        [
            # parse_comments=True
            ('BOOL_TRUE_STRING_LIKE_BOOL_WITH_COMMENT', 'True', "'True' # comment\n", True),
            ('BOOL_TRUE_BOOL_WITH_COMMENT', 'True ', "True # comment\n", True),
            ('STR_QUOTED_IGNORE_COMMENT', 'foo', " 'foo' # comment\n", True),
            ('STR_QUOTED_INCLUDE_HASH', 'foo # with hash', "'foo # with hash' # not comment\n", True),
            ('SECRET_KEY_1', '"abc', '"abc#def"\n', True),
            ('SECRET_KEY_2', 'abc', 'abc#def\n', True),
            ('SECRET_KEY_3', 'abc#def', "'abc#def'\n",  True),

            # parse_comments=False
            ('BOOL_TRUE_STRING_LIKE_BOOL_WITH_COMMENT', "'True' # comment", "'True' # comment\n", False),
            ('BOOL_TRUE_BOOL_WITH_COMMENT', 'True # comment', "True # comment\n", False),
            ('STR_QUOTED_IGNORE_COMMENT', " 'foo' # comment", " 'foo' # comment\n", False),
            ('STR_QUOTED_INCLUDE_HASH', "'foo # with hash' # not comment", "'foo # with hash' # not comment\n", False),
            ('SECRET_KEY_1', 'abc#def', '"abc#def"\n', False),
            ('SECRET_KEY_2', 'abc#def', 'abc#def\n', False),
            ('SECRET_KEY_3', 'abc#def', "'abc#def'\n",  False),

            # parse_comments is not defined (default behavior)
            ('BOOL_TRUE_STRING_LIKE_BOOL_WITH_COMMENT', "'True' # comment", "'True' # comment\n", None),
            ('BOOL_TRUE_BOOL_WITH_COMMENT', 'True # comment', "True # comment\n", None),
            ('STR_QUOTED_IGNORE_COMMENT', " 'foo' # comment", " 'foo' # comment\n", None),
            ('STR_QUOTED_INCLUDE_HASH', "'foo # with hash' # not comment", "'foo # with hash' # not comment\n", None),
            ('SECRET_KEY_1', 'abc#def', '"abc#def"\n', None),
            ('SECRET_KEY_2', 'abc#def', 'abc#def\n', None),
            ('SECRET_KEY_3', 'abc#def', "'abc#def'\n",  None),
        ],
    )
def test_parse_comments(variable, value, raw_value, parse_comments):
    old_environ = os.environ

    with tempfile.TemporaryDirectory() as temp_dir:
        env_path = os.path.join(temp_dir, '.env')

        with open(env_path, 'w') as f:
            f.write(f'{variable}={raw_value}\n')
            f.flush()

            env = Env()
            Env.ENVIRON = {}
            if parse_comments is None:
                env.read_env(env_path)
            else:
                env.read_env(env_path, parse_comments=parse_comments)

            assert env(variable) == value

    os.environ = old_environ


class TestEnv:
    def setup_method(self, method):
        """
        Setup environment variables.

        Setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.old_environ = os.environ
        os.environ = Env.ENVIRON = FakeEnv.generate_data()
        self.env = Env()

    def teardown_method(self, method):
        """
        Rollback environment variables.

        Teardown any state that was previously setup with a setup_method call.
        """
        assert self.old_environ is not None
        os.environ = self.old_environ

    def test_not_present_with_default(self):
        assert self.env('not_present', default=3) == 3

    def test_not_present_without_default(self):
        with pytest.raises(ImproperlyConfigured) as excinfo:
            self.env('not_present')
        assert str(excinfo.value) == 'Set the not_present environment variable'
        assert excinfo.value.__cause__ is not None

    def test_contains(self):
        assert 'STR_VAR' in self.env
        assert 'EMPTY_LIST' in self.env
        assert 'I_AM_NOT_A_VAR' not in self.env

    @pytest.mark.parametrize(
        'var,val,multiline',
        [
            ('STR_VAR', 'bar', False),
            ('MULTILINE_STR_VAR', 'foo\\nbar', False),
            ('MULTILINE_STR_VAR', 'foo\nbar', True),
            ('MULTILINE_QUOTED_STR_VAR', '---BEGIN---\\r\\n---END---', False),
            ('MULTILINE_QUOTED_STR_VAR', '---BEGIN---\n---END---', True),
            ('MULTILINE_ESCAPED_STR_VAR', '---BEGIN---\\\\n---END---', False),
            ('MULTILINE_ESCAPED_STR_VAR', '---BEGIN---\\\n---END---', True),
        ],
    )
    def test_str(self, var, val, multiline):
        assert isinstance(self.env(var), str)
        if not multiline:
            assert self.env(var) == val
        assert self.env.str(var, multiline=multiline) == val

    @pytest.mark.parametrize(
        'var,val,default',
        [
            ('STR_VAR', b'bar', Env.NOTSET),
            ('NON_EXISTENT_BYTES_VAR', b'some-default', b'some-default'),
            ('NON_EXISTENT_STR_VAR', b'some-default', 'some-default'),
        ]
    )
    def test_bytes(self, var, val, default):
        assert_type_and_value(bytes, val, self.env.bytes(var, default=default))

    def test_int(self):
        assert_type_and_value(int, 42, self.env('INT_VAR', cast=int))
        assert_type_and_value(int, 42, self.env.int('INT_VAR'))

    def test_int_with_none_default(self):
        assert self.env('NOT_PRESENT_VAR', cast=int, default=None) is None
        assert self.env('EMPTY_INT_VAR', cast=int, default=None) is None

    @pytest.mark.parametrize(
        'value,variable',
        [
            (33.3, 'FLOAT_VAR'),
            (33.3, 'FLOAT_COMMA_VAR'),
            (123420333.3, 'FLOAT_STRANGE_VAR1'),
            (123420333.3, 'FLOAT_STRANGE_VAR2'),
            (-1.0, 'FLOAT_NEGATIVE_VAR'),
        ]
    )
    def test_float(self, value, variable):
        assert_type_and_value(float, value, self.env.float(variable))
        assert_type_and_value(float, value, self.env(variable, cast=float))

    @pytest.mark.parametrize(
        'value,variable',
        [
            (True, 'BOOL_TRUE_STRING_LIKE_INT'),
            (True, 'BOOL_TRUE_STRING_LIKE_BOOL'),
            (True, 'BOOL_TRUE_INT'),
            (True, 'BOOL_TRUE_BOOL'),
            (True, 'BOOL_TRUE_STRING_1'),
            (True, 'BOOL_TRUE_STRING_2'),
            (True, 'BOOL_TRUE_STRING_3'),
            (True, 'BOOL_TRUE_STRING_4'),
            (True, 'BOOL_TRUE_STRING_5'),
            (False, 'BOOL_FALSE_STRING_LIKE_INT'),
            (False, 'BOOL_FALSE_INT'),
            (False, 'BOOL_FALSE_STRING_LIKE_BOOL'),
            (False, 'BOOL_FALSE_BOOL'),
        ]
    )
    def test_bool_true(self, value, variable):
        assert_type_and_value(bool, value, self.env.bool(variable))
        assert_type_and_value(bool, value, self.env(variable, cast=bool))

    def test_proxied_value(self):
        assert self.env('PROXIED_VAR') == 'bar'

    def test_escaped_dollar_sign(self):
        self.env.escape_proxy = True
        assert self.env('ESCAPED_VAR') == '$baz'

    def test_escaped_dollar_sign_disabled(self):
        self.env.escape_proxy = False
        assert self.env('ESCAPED_VAR') == r'\$baz'

    def test_int_list(self):
        assert_type_and_value(list, [42, 33], self.env('INT_LIST', cast=[int]))
        assert_type_and_value(list, [42, 33], self.env.list('INT_LIST', int))

    def test_int_list_cast_tuple(self):
        assert_type_and_value(tuple, (42, 33), self.env('INT_LIST', cast=(int,)))
        assert_type_and_value(tuple, (42, 33), self.env.tuple('INT_LIST', int))
        assert_type_and_value(tuple, ('42', '33'), self.env.tuple('INT_LIST'))

    def test_int_tuple(self):
        assert_type_and_value(tuple, (42, 33), self.env('INT_TUPLE', cast=(int,)))
        assert_type_and_value(tuple, (42, 33), self.env.tuple('INT_TUPLE', int))
        assert_type_and_value(tuple, ('42', '33'), self.env.tuple('INT_TUPLE'))

    def test_mix_tuple_issue_387(self):
        """Cast a tuple of mixed types.

        Casts a string like "(42,Test)" to a tuple like  (42, 'Test').
        See: https://github.com/joke2k/django-environ/issues/387 for details."""
        assert_type_and_value(
            tuple,
            (42, 'Test'),
            self.env(
                'MIX_TUPLE',
                default=(0, ''),
                cast=lambda t: tuple(
                    map(
                        lambda v: int(v) if v.isdigit() else v.strip(),
                        [c for c in t.strip('()').split(',')]
                    )
                ),
            )
        )

    def test_str_list_with_spaces(self):
        assert_type_and_value(list, [' foo', '  spaces'],
                              self.env('STR_LIST_WITH_SPACES', cast=[str]))
        assert_type_and_value(list, [' foo', '  spaces'],
                              self.env.list('STR_LIST_WITH_SPACES'))

    def test_empty_list(self):
        assert_type_and_value(list, [], self.env('EMPTY_LIST', cast=[int]))

    def test_dict_value(self):
        assert_type_and_value(dict, FakeEnv.DICT, self.env.dict('DICT_VAR'))
        assert_type_and_value(dict, FakeEnv.DICT_WITH_EQ, self.env.dict('DICT_WITH_EQ_VAR'))

    def test_complex_dict_value(self):
        assert_type_and_value(
            dict,
            FakeEnv.SAML_ATTRIBUTE_MAPPING,
            self.env.dict('SAML_ATTRIBUTE_MAPPING', cast={'value': tuple})
        )

    @pytest.mark.parametrize(
        'value,cast,expected',
        [
            ('a=1', dict, {'a': '1'}),
            ('a=1', dict(value=int), {'a': 1}),
            ('a=1', dict(value=float), {'a': 1.0}),
            ('a=1,2,3', dict(value=[str]), {'a': ['1', '2', '3']}),
            ('a=1,2,3', dict(value=[int]), {'a': [1, 2, 3]}),
            ('a=1;b=1.1,2.2;c=3', dict(value=int, cast=dict(b=[float])),
             {'a': 1, 'b': [1.1, 2.2], 'c': 3}),
            ('a=uname;c=http://www.google.com;b=True',
             dict(value=str, cast=dict(b=bool)),
             {'a': "uname", 'c': "http://www.google.com", 'b': True}),
        ],
        ids=[
            'dict',
            'dict_int',
            'dict_float',
            'dict_str_list',
            'dict_int_list',
            'dict_int_cast',
            'dict_str_cast',
        ],
    )
    def test_dict_parsing(self, value, cast, expected):
        assert self.env.parse_value(value, cast) == expected

    def test_url_value(self):
        url = self.env.url('URL_VAR')
        assert url.__class__ == self.env.URL_CLASS
        assert url.geturl() == FakeEnv.URL
        assert self.env.url('OTHER_URL', default=None) is None

    def test_url_empty_string_default_value(self):
        unset_var_name = 'VARIABLE_NOT_SET_IN_ENVIRONMENT'
        assert unset_var_name not in os.environ
        url = self.env.url(unset_var_name, '')
        assert url.__class__ == self.env.URL_CLASS
        assert url.geturl() == ''

    def test_url_encoded_parts(self):
        password_with_unquoted_characters = "#password"
        encoded_url = "mysql://user:%s@127.0.0.1:3306/dbname" % quote(
            password_with_unquoted_characters
        )
        parsed_url = self.env.db_url_config(encoded_url)
        assert parsed_url['PASSWORD'] == password_with_unquoted_characters

    @pytest.mark.parametrize(
        'var,engine,name,host,user,passwd,port',
        [
            (Env.DEFAULT_DATABASE_ENV, DJANGO_POSTGRES, 'd8r82722',
             'ec2-107-21-253-135.compute-1.amazonaws.com', 'uf07k1',
             'wegauwhg', 5431),
            ('DATABASE_MYSQL_URL', 'django.db.backends.mysql', 'heroku_97681',
             'us-cdbr-east.cleardb.com', 'bea6eb0', '69772142', ''),
            ('DATABASE_MYSQL_GIS_URL', 'django.contrib.gis.db.backends.mysql',
             'some_database', '127.0.0.1', 'user', 'password', ''),
            ('DATABASE_ORACLE_TNS_URL', 'django.db.backends.oracle', 'sid', '',
             'user', 'password', None),
            ('DATABASE_ORACLE_URL', 'django.db.backends.oracle', 'sid', 'host',
             'user', 'password', '1521'),
            ('DATABASE_REDSHIFT_URL', 'django_redshift_backend', 'dev',
             'examplecluster.abc123xyz789.us-west-2.redshift.amazonaws.com',
             'user', 'password', 5439),
            ('DATABASE_SQLITE_URL', 'django.db.backends.sqlite3',
             '/full/path/to/your/database/file.sqlite', '', '', '', ''),
            ('DATABASE_CUSTOM_BACKEND_URL', 'custom.backend', 'database',
             'example.com', 'user', 'password', 5430),
            ('DATABASE_MYSQL_CLOUDSQL_URL', 'django.db.backends.mysql', 'mydatabase',
             '/cloudsql/arvore-codelab:us-central1:mysqlinstance', 'djuser', 'hidden-password', ''),
        ],
        ids=[
            'postgres',
            'mysql',
            'mysql_gis',
            'oracle_tns',
            'oracle',
            'redshift',
            'sqlite',
            'custom',
            'cloudsql',
        ],
    )
    def test_db_url_value(self, var, engine, name, host, user, passwd, port):
        config = self.env.db(var)

        assert config['ENGINE'] == engine
        assert config['NAME'] == name
        assert config['HOST'] == host
        assert config['USER'] == user
        assert config['PASSWORD'] == passwd

        if port is None:
            assert 'PORT' not in config
        else:
            assert config['PORT'] == port

    @pytest.mark.parametrize(
        'var,backend,location,options',
        [
            (Env.DEFAULT_CACHE_ENV,
             'django.core.cache.backends.memcached.MemcachedCache',
             '127.0.0.1:11211', None),
            ('CACHE_REDIS', REDIS_DRIVER,
             'redis://127.0.0.1:6379/1',
             {'CLIENT_CLASS': 'django_redis.client.DefaultClient',
              'PASSWORD': 'secret'}),
        ],
        ids=[
            'memcached',
            'redis',
        ],
    )
    def test_cache_url_value(self, var, backend, location, options):
        config = self.env.cache_url(var)

        assert config['BACKEND'] == backend
        assert config['LOCATION'] == location

        if options is None:
            assert 'OPTIONS' not in config
        else:
            assert config['OPTIONS'] == options

    def test_email_url_value(self):
        email_config = self.env.email_url()
        assert email_config['EMAIL_BACKEND'] == (
            'django.core.mail.backends.smtp.EmailBackend'
        )
        assert email_config['EMAIL_HOST'] == 'smtp.example.com'
        assert email_config['EMAIL_HOST_PASSWORD'] == 'password'
        assert email_config['EMAIL_HOST_USER'] == 'user@domain.com'
        assert email_config['EMAIL_PORT'] == 587
        assert email_config['EMAIL_USE_TLS']

    def test_json_value(self):
        assert self.env.json('JSON_VAR') == FakeEnv.JSON

    def test_path(self):
        root = self.env.path('PATH_VAR')
        assert_type_and_value(Path, Path(FakeEnv.PATH), root)

    def test_smart_cast(self):
        assert self.env.get_value('STR_VAR', default='string') == 'bar'
        assert self.env.get_value('BOOL_TRUE_STRING_LIKE_INT', default=True)
        assert not self.env.get_value(
            'BOOL_FALSE_STRING_LIKE_INT',
            default=True)
        assert self.env.get_value('INT_VAR', default=1) == 42
        assert self.env.get_value('FLOAT_VAR', default=1.2) == 33.3

    def test_exported(self):
        assert self.env('EXPORTED_VAR') == FakeEnv.EXPORTED

    def test_prefix(self):
        self.env.prefix = 'PREFIX_'
        assert self.env('TEST') == 'foo'

    def test_prefix_and_not_present_without_default(self):
        self.env.prefix = 'PREFIX_'
        with pytest.raises(ImproperlyConfigured) as excinfo:
            self.env('not_present')
        assert str(excinfo.value) == 'Set the PREFIX_not_present environment variable'
        assert excinfo.value.__cause__ is not None


class TestFileEnv(TestEnv):
    def setup_method(self, method):
        """
        Setup environment variables.

        Setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        super().setup_method(method)

        Env.ENVIRON = {}
        self.env.read_env(
            Path(__file__, is_file=True)('test_env.txt'),
            PATH_VAR=Path(__file__, is_file=True).__root__
        )

    def create_temp_env_file(self, name):
        import pathlib
        import tempfile

        env_file_path = (pathlib.Path(tempfile.gettempdir()) / name)
        try:
            env_file_path.unlink()
        except FileNotFoundError:
            pass

        assert not env_file_path.exists()
        return env_file_path

    def test_read_env_path_like(self):
        env_file_path = self.create_temp_env_file('test_pathlib.env')

        env_key = 'SECRET'
        env_val = 'enigma'
        env_str = env_key + '=' + env_val

        # open() doesn't take path-like on Python < 3.6
        with open(str(env_file_path), 'w', encoding='utf-8') as f:
            f.write(env_str + '\n')

        self.env.read_env(env_file_path)
        assert env_key in self.env.ENVIRON
        assert self.env.ENVIRON[env_key] == env_val

    @pytest.mark.parametrize("overwrite", [True, False])
    def test_existing_overwrite(self, overwrite):
        env_file_path = self.create_temp_env_file('test_existing.env')
        with open(str(env_file_path), 'w') as f:
            f.write("EXISTING=b")
        self.env.ENVIRON['EXISTING'] = "a"
        self.env.read_env(env_file_path, overwrite=overwrite)
        assert self.env.ENVIRON["EXISTING"] == ("b" if overwrite else "a")


class TestSubClass(TestEnv):
    def setup_method(self, method):
        """
        Setup environment variables.

        Setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        super().setup_method(method)

        self.CONFIG = FakeEnv.generate_data()

        class MyEnv(Env):
            ENVIRON = self.CONFIG

        self.env = MyEnv()

    def test_singleton_environ(self):
        assert self.CONFIG is self.env.ENVIRON
