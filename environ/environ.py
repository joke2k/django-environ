"""
Django-environ allows you to utilize 12factor inspired environment
variables to configure your Django application.
"""
from __future__ import unicode_literals
import os
import sys
import re
import json
import warnings

import logging

logger = logging.getLogger(__file__)

try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass

try:
    import urllib.parse as urlparse
except ImportError:
    # Python <= 2.6
    import urlparse


if sys.version < '3':
    text_type = unicode
else:
    text_type = str
    basestring = str


__author__ = 'joke2k'
__version__ = (0, 3, 1)


# return int if possible
_cast_int = lambda v: int(v) if isinstance(v, basestring) and v.isdigit() else v
# return str if possibile
_cast_str = lambda v: str(v) if isinstance(v, basestring) else v


class NoValue(object):
    def __repr__(self):
        return '<{0}>'.format(self.__class__.__name__)


class Env(object):
    """Provide schema-based lookups of environment variables so that each
    caller doesn't have to pass in `cast` and `default` parameters.

    Usage:::

        env = Env(MAIL_ENABLED=bool, SMTP_LOGIN=(str, 'DEFAULT'))
        if env('MAIL_ENABLED'):
            ...
    """

    NOTSET = NoValue()
    BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1')
    URL_CLASS = urlparse.ParseResult
    DEFAULT_DATABASE_ENV = 'DATABASE_URL'
    DB_SCHEMES = {
        'postgres': 'django.db.backends.postgresql_psycopg2',
        'postgresql': 'django.db.backends.postgresql_psycopg2',
        'psql': 'django.db.backends.postgresql_psycopg2',
        'pgsql': 'django.db.backends.postgresql_psycopg2',
        'postgis': 'django.contrib.gis.db.backends.postgis',
        'mysql': 'django.db.backends.mysql',
        'mysql2': 'django.db.backends.mysql',
        'mysqlgis': 'django.contrib.gis.db.backends.mysql',
        'spatialite': 'django.contrib.gis.db.backends.spatialite',
        'sqlite': 'django.db.backends.sqlite3',
        'ldap': 'ldapdb.backends.ldap',
    }
    _DB_BASE_OPTIONS = ['CONN_MAX_AGE', 'ATOMIC_REQUESTS', 'AUTOCOMMIT']

    DEFAULT_CACHE_ENV = 'CACHE_URL'
    CACHE_SCHEMES = {
        'dbcache': 'django.core.cache.backends.db.DatabaseCache',
        'dummycache': 'django.core.cache.backends.dummy.DummyCache',
        'filecache': 'django.core.cache.backends.filebased.FileBasedCache',
        'locmemcache': 'django.core.cache.backends.locmem.LocMemCache',
        'memcache': 'django.core.cache.backends.memcached.MemcachedCache',
        'pymemcache': 'django.core.cache.backends.memcached.PyLibMCCache',
        'rediscache': 'redis_cache.cache.RedisCache',
        'redis': 'redis_cache.cache.RedisCache',
    }
    _CACHE_BASE_OPTIONS = ['TIMEOUT', 'KEY_PREFIX', 'VERSION', 'KEY_FUNCTION']

    DEFAULT_EMAIL_ENV = 'EMAIL_URL'
    EMAIL_SCHEMES = {
        'smtp': 'django.core.mail.backends.smtp.EmailBackend',
        'smtps': 'django.core.mail.backends.smtp.EmailBackend',
        'consolemail': 'django.core.mail.backends.console.EmailBackend',
        'filemail': 'django.core.mail.backends.filebased.EmailBackend',
        'memorymail': 'django.core.mail.backends.locmem.EmailBackend',
        'dummymail': 'django.core.mail.backends.dummy.EmailBackend'
    }
    _EMAIL_BASE_OPTIONS = ['EMAIL_USE_TLS', ]

    DEFAULT_SEARCH_ENV = 'SEARCH_URL'
    SEARCH_SCHEMES = {
        "elasticsearch": "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine",
        "solr": "haystack.backends.solr_backend.SolrEngine",
        "whoosh": "haystack.backends.whoosh_backend.WhooshEngine",
        "simple": "haystack.backends.simple_backend.SimpleEngine",
    }



    def __init__(self, **schema):
        self.schema = schema

    def __call__(self, var, cast=None, default=NOTSET, parse_default=False):
        return self.get_value(var, cast=cast, default=default, parse_default=parse_default)

    # Shortcuts

    def str(self, var, default=NOTSET):
        """
        :rtype: str
        """
        return self.get_value(var, default=default)

    def unicode(self, var, default=NOTSET):
        """Helper for python2
        :rtype: unicode
        """
        return self.get_value(var, cast=text_type, default=default)

    def bool(self, var, default=NOTSET):
        """
        :rtype: bool
        """
        return self.get_value(var, cast=bool, default=default)

    def int(self, var, default=NOTSET):
        """
        :rtype: int
        """
        return self.get_value(var, cast=int, default=default)

    def float(self, var, default=NOTSET):
        """
        :rtype: float
        """
        return self.get_value(var, cast=float, default=default)

    def json(self, var, default=NOTSET):
        """
        :returns: Json parsed
        """
        return self.get_value(var, cast=json.loads, default=default)

    def list(self, var, cast=None, default=NOTSET):
        """
        :rtype: list
        """
        return self.get_value(var, cast=list if not cast else [cast], default=default)

    def dict(self, var, cast=dict, default=NOTSET):
        """
        :rtype: dict
        """
        return self.get_value(var, cast=cast, default=default)

    def url(self, var, default=NOTSET):
        """
        :rtype: urlparse.ParseResult
        """
        return self.get_value(var, cast=urlparse.urlparse, default=default, parse_default=True)

    def db_url(self, var=DEFAULT_DATABASE_ENV, default=NOTSET, engine=None):
        """Returns a config dictionary, defaulting to DATABASE_URL.

        :rtype: dict
        """
        return self.db_url_config(self.get_value(var, default=default), engine=engine)
    db=db_url

    def cache_url(self, var=DEFAULT_CACHE_ENV, default=NOTSET, backend=None):
        """Returns a config dictionary, defaulting to CACHE_URL.

        :rtype: dict
        """
        return self.cache_url_config(self.url(var, default=default), backend=backend)
    cache=cache_url

    def email_url(self, var=DEFAULT_EMAIL_ENV, default=NOTSET, backend=None):
        """Returns a config dictionary, defaulting to EMAIL_URL.

        :rtype: dict
        """
        return self.email_url_config(self.url(var, default=default), backend=backend)
    email=email_url

    def search_url(self, var=DEFAULT_SEARCH_ENV, default=NOTSET, engine=None):
        """Returns a config dictionary, defaulting to SEARCH_URL.

        :rtype: dict
        """
        return self.search_url_config(self.url(var, default=default), engine=engine)

    def path(self, var, default=NOTSET, **kwargs):
        """
        :rtype: Path
        """
        return Path(self.get_value(var, default=default), **kwargs)

    def get_value(self, var, cast=None, default=NOTSET, parse_default=False):
        """Return value for given environment variable.

        :param var: Name of variable.
        :param cast: Type to cast return value as.
        :param default: If var not present in environ, return this instead.
        :param parse_default: force to parse default..

        :returns: Value from environment or default (if set)
        """

        logger.debug("get '{0}' casted as '{1}' with default '{2}'".format(var, cast, default))

        if var in self.schema:
            var_info = self.schema[var]

            try:
                has_default = len(var_info) == 2
            except TypeError:
                has_default = False

            if has_default:
                if not cast:
                    cast = var_info[0]

                if default is self.NOTSET:
                    try:
                        default = var_info[1]
                    except IndexError:
                        pass
            else:
                if not cast:
                    cast = var_info

        try:
            value = os.environ[var]
        except KeyError:
            if default is self.NOTSET:
                error_msg = "Set the {0} environment variable".format(var)
                raise ImproperlyConfigured(error_msg)

            value = default

        # Resolve any proxied values
        if hasattr(value, 'startswith') and value.startswith('$'):
            value = value.lstrip('$')
            value = self.get_value(value, cast=cast, default=default)

        if value != default or parse_default:
            value = self.parse_value(value, cast)

        return value

    # Class and static methods

    @classmethod
    def parse_value(cls, value, cast):
        """Parse and cast provided value

        :param value: Stringed value.
        :param cast: Type to cast return value as.

        :returns: Casted value
        """
        if cast is None:
            return value
        elif cast is bool:
            try:
                value = int(value) != 0
            except ValueError:
                value = value.lower() in cls.BOOLEAN_TRUE_STRINGS
        elif isinstance(cast, list):
            value = list(map(cast[0], [x for x in value.split(',') if x]))
        elif isinstance(cast, dict):
            key_cast = cast.get('key', str)
            value_cast = cast.get('value', text_type)
            value_cast_by_key = cast.get('cast', dict())
            value = dict(map(
                lambda kv: (key_cast(kv[0]), cls.parse_value(kv[1], value_cast_by_key.get(kv[0], value_cast))),
                [val.split('=') for val in value.split(';') if val]
            ))
        elif cast is dict:
        #elif hasattr(cast, '__name__') and cast.__name__ == 'dict':
            value = dict([val.split('=') for val in value.split(',') if val])
        elif cast is list:
            value = [x for x in value.split(',') if x]
        elif cast is float:
            # clean string
            float_str = re.sub(r'[^\d,\.]', '', value)
            # split for avoid thousand separator and different locale comma/dot symbol
            parts = re.split(r'[,\.]', float_str)
            if len(parts) == 1:
                float_str = parts[0]
            else:
                float_str = "{0}.{1}".format(''.join(parts[0:-1]), parts[-1])
            value = float(float_str)
        else:
            value = cast(value)
        return value

    @classmethod
    def db_url_config(cls, url, engine=None):
        """Pulled from DJ-Database-URL, parse an arbitrary Database URL.
        Support currently exists for PostgreSQL, PostGIS, MySQL and SQLite.

        SQLite connects to file based databases. The same URL format is used, omitting the hostname,
        and using the "file" portion as the filename of the database.
        This has the effect of four slashes being present for an absolute file path:

        >>> from environ import Env
        >>> Env.db_url_config('sqlite:////full/path/to/your/file.sqlite')
        {'ENGINE': 'django.db.backends.sqlite3', 'HOST': None, 'NAME': '/full/path/to/your/file.sqlite', 'PASSWORD': None, 'PORT': None, 'USER': None}
        >>> Env.db_url_config('postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn')
        {'ENGINE': 'django.db.backends.postgresql_psycopg2', 'HOST': 'ec2-107-21-253-135.compute-1.amazonaws.com', 'NAME': 'd8r82722r2kuvn', 'PASSWORD': 'wegauwhgeuioweg', 'PORT': 5431, 'USER': 'uf07k1i6d8ia0v'}

        """
        if not isinstance(url, cls.URL_CLASS):
            if url == 'sqlite://:memory:':
                # this is a special case, because if we pass this URL into
                # urlparse, urlparse will choke trying to interpret "memory"
                # as a port number
                return {
                    'ENGINE': cls.DB_SCHEMES['sqlite'],
                    'NAME': ':memory:'
                }
                # note: no other settings are required for sqlite
            url = urlparse.urlparse(url)

        config = {}

        # Remove query strings.
        path = url.path[1:]
        path = path.split('?', 2)[0]

        # if we are using sqlite and we have no path, then assume we
        # want an in-memory database (this is the behaviour of sqlalchemy)
        if url.scheme == 'sqlite' and path == '':
            path = ':memory:'
        if url.scheme == 'ldap':
            path = '{scheme}://{hostname}'.format(scheme=_cast_str(url.scheme), hostname=_cast_str(url.hostname))
            if url.port:
                path += ':{port}'.format(port=_cast_str(url.port))

        # Update with environment configuration.
        config.update({
            'NAME': path,
            'USER': _cast_str(url.username),
            'PASSWORD': _cast_str(url.password),
            'HOST': _cast_str(url.hostname),
            'PORT': _cast_int(url.port),
        })

        if url.query:
            config_options = {}
            for k, v in urlparse.parse_qs(url.query).items():
                if k.upper() in cls._DB_BASE_OPTIONS:
                    config.update({k.upper(): _cast_int(v[0])})
                else:
                    config_options.update({k: _cast_int(v[0])})
            config['OPTIONS'] = config_options

        if engine:
            config['ENGINE'] = engine
        if url.scheme in Env.DB_SCHEMES:
            config['ENGINE'] = Env.DB_SCHEMES[url.scheme]

        if not config.get('ENGINE', False):
            warnings.warn("Engine not recognized from url: {0}".format(config))
            return {}

        return config

    @classmethod
    def cache_url_config(cls, url, backend=None):
        """Pulled from DJ-Cache-URL, parse an arbitrary Cache URL.

        :param url:
        :param overrides:
        :return:
        """
        url = urlparse.urlparse(url) if not isinstance(url, cls.URL_CLASS) else url

        location = url.netloc.split(',')
        if len(location) == 1:
            location = location[0]

        config = {
            'BACKEND': cls.CACHE_SCHEMES[url.scheme],
            'LOCATION': location,
        }

        if url.scheme == 'filecache':
            config.update({
                'LOCATION': _cast_str(url.netloc + url.path),
            })

        if url.path and url.scheme in ['memcache', 'pymemcache', 'rediscache']:
            config.update({
                'LOCATION': 'unix:' + url.path,
            })

        if url.query:
            config_options = {}
            for k, v in urlparse.parse_qs(url.query).items():
                opt = {k.upper(): _cast_int(v[0])}
                if k.upper() in cls._CACHE_BASE_OPTIONS:
                    config.update(opt)
                else:
                    config_options.update(opt)
            config['OPTIONS'] = config_options

        if backend:
            config['BACKEND'] = backend

        return config

    @classmethod
    def email_url_config(cls, url, backend=None):
        """Parses an email URL."""

        config = {}

        url = urlparse.urlparse(url) if not isinstance(url, cls.URL_CLASS) else url

        # Remove query strings
        path = url.path[1:]
        path = path.split('?', 2)[0]

        # Update with environment configuration
        config.update({
            'EMAIL_FILE_PATH': path,
            'EMAIL_HOST_USER': _cast_str(url.username),
            'EMAIL_HOST_PASSWORD': _cast_str(url.password),
            'EMAIL_HOST': _cast_str(url.hostname),
            'EMAIL_PORT': _cast_int(url.port),
        })

        if backend:
            config['EMAIL_BACKEND'] = backend
        elif url.scheme in cls.EMAIL_SCHEMES:
            config['EMAIL_BACKEND'] = cls.EMAIL_SCHEMES[url.scheme]

        if url.scheme == 'smtps':
            config['EMAIL_USE_TLS'] = True
        else:
            config['EMAIL_USE_TLS'] = False

        if url.query:
            config_options = {}
            for k, v in urlparse.parse_qs(url.query).items():
                opt = {k.upper(): _cast_int(v[0])}
                if k.upper() in cls._EMAIL_BASE_OPTIONS:
                    config.update(opt)
                else:
                    config_options.update(opt)
            config['OPTIONS'] = config_options

        return config

    @classmethod
    def search_url_config(cls, url, engine=None):
        config = {}

        url = urlparse.urlparse(url) if not isinstance(url, cls.URL_CLASS) else url

        # Remove query strings.
        path = url.path[1:]
        path = path.split('?', 2)[0]

        if url.scheme in cls.SEARCH_SCHEMES:
            config["ENGINE"] = cls.SEARCH_SCHEMES[url.scheme]

        if path.endswith("/"):
            path = path[:-1]

        split = path.rsplit("/", 1)

        if len(split) > 1:
            path = split[:-1]
            index = split[-1]
        else:
            path = ""
            index = split[0]

        config.update({
            "URL": urlparse.urlunparse(("http",) + url[1:2] + (path,) + url[3:]),
            "INDEX_NAME": index,
            })

        if path:
            config.update({
                "PATH": path,
            })

        if engine:
            config['ENGINE'] = engine

        return config

    @staticmethod
    def read_env(env_file=None, **overrides):
        """Read a .env file into os.environ.

        If not given a path to a dotenv path, does filthy magic stack backtracking
        to find manage.py and then find the dotenv.

        http://www.wellfireinteractive.com/blog/easier-12-factor-django/

        https://gist.github.com/bennylope/2999704
        """
        if env_file is None:
            frame = sys._getframe()
            env_file = os.path.join(os.path.dirname(frame.f_back.f_code.co_filename), '.env')
            if not os.path.exists(env_file):
                warnings.warn("not reading %s - it doesn't exist." % env_file)
                return

        try:
            with open(env_file) if isinstance(env_file, basestring) else env_file as f:
                content = f.read()
        except IOError:
            warnings.warn("not reading %s - it doesn't exist." % env_file)
            return

        logger.debug('Read environment variables from: {0}'.format(env_file))

        for line in content.splitlines():
            m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
            if m1:
                key, val = m1.group(1), m1.group(2)
                m2 = re.match(r"\A'(.*)'\Z", val)
                if m2:
                    val = m2.group(1)
                m3 = re.match(r'\A"(.*)"\Z', val)
                if m3:
                    val = re.sub(r'\\(.)', r'\1', m3.group(1))
                os.environ.setdefault(key, text_type(val))

        # set defaults
        for key, value in overrides.items():
            os.environ.setdefault(key, value)


class Path(object):
    """Inspired to Django Two-scoops, handling File Paths in Settings.

        >>> from environ import Path
        >>> root = Path('/home')
        >>> root, root(), root('dev')
        (<Path:/home>, '/home', '/home/dev')
        >>> root == Path('/home')
        True
        >>> root in Path('/'), root not in Path('/other/path')
        (True, True)
        >>> root('dev', 'not_existing_dir', required=True)
        Traceback (most recent call last):
        environ.environ.ImproperlyConfigured: Create required path: /home/not_existing_dir
        >>> public = root.path('public')
        >>> public, public.root, public('styles')
        (<Path:/home/public>, '/home/public', '/home/public/styles')
        >>> assets, scripts = public.path('assets'), public.path('assets', 'scripts')
        >>> assets.root, scripts.root
        ('/home/public/assets', '/home/public/assets/scripts')
        >>> assets + 'styles', str(assets + 'styles'), ~assets
        (<Path:/home/public/assets/styles>, '/home/public/assets/styles', <Path:/home/public>)

    """

    def path(self, *paths, **kwargs):
        """Create new Path based on self.root and provided paths.

        :param paths: List of sub paths
        :param kwargs: required=False
        :rtype: Path
        """
        return self.__class__(self.__root__, *paths, **kwargs)

    def file(self, name, *args, **kwargs):
        """Open a file.

        :param name: Filename appended to self.root
        :param args: passed to open()
        :param kwargs: passed to open()

        :rtype: file
        """
        return open(self(name), *args, **kwargs)

    @property
    def root(self):
        """Current directory for this Path"""
        return self.__root__

    def __init__(self, start='', *paths, **kwargs):

        super(Path, self).__init__()

        if kwargs.get('is_file', False):
            start = os.path.dirname(start)

        self.__root__ = self._absolute_join(start, *paths, **kwargs)

    def __call__(self, *paths, **kwargs):
        """Retrieve the absolute path, with appended paths

        :param paths: List of sub path of self.root
        :param kwargs: required=False
        """
        return self._absolute_join(self.__root__, *paths, **kwargs)

    def __eq__(self, other):
        return self.__root__ == other.__root__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Path(self.__root__, other if not isinstance(other, Path) else other.__root__)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.path('../' * other)
        elif isinstance(other, (str, text_type)):
            return Path(self.__root__.rstrip(other))
        raise TypeError("unsupported operand type(s) for -: '{0}' and '{1}'".format(self, type(other)))

    def __invert__(self):
        return self.path('..')

    def __contains__(self, item):
        base_path = self.__root__
        if len(base_path) > 1:
            base_path = os.path.join(base_path, '')
        return item.__root__.startswith(base_path)

    def __repr__(self):
        return "<Path:{0}>".format(self.__root__)

    def __str__(self):
        return self.__root__

    def __unicode__(self):
        return self.__str__()

    @staticmethod
    def _absolute_join(base, *paths, **kwargs):
        absolute_path = os.path.abspath(os.path.join(base, *paths))
        if kwargs.get('required', False) and not os.path.exists(absolute_path):
            raise ImproperlyConfigured("Create required path: {0}".format(absolute_path))
        return absolute_path

def register_scheme(scheme):
    for method in filter(lambda s: s.startswith('uses_'), dir(urlparse)):
        getattr(urlparse, method).append(scheme)

# Register database and cache schemes in URLs.
for schema in list(Env.DB_SCHEMES.keys()) + list(Env.CACHE_SCHEMES.keys()) + list(Env.SEARCH_SCHEMES.keys()) +list(Env.EMAIL_SCHEMES.keys()):
    register_scheme(schema)
