"""
Django-environ allows you to utilize 12factor inspired environment
variables to configure your Django application.

This module is a merge of:

* https://github.com/rconradharris/envparse
* https://github.com/kennethreitz/dj-database-url
* https://github.com/nickstenning/honcho

and inspired by:

* http://www.12factor.net/
* http://www.wellfireinteractive.com/blog/easier-12-factor-django/
* https://django.2scoops.org (book)

"""
import os
import re
import json

import logging
logger = logging.getLogger(__file__)

try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


__author__ = 'joke2k'
__version__ = (0, 2)


class Env(object):
    """Provide schema-based lookups of environment variables so that each
    caller doesn't have to pass in `cast` and `default` parameters.

    Usage:::

        env = Env(MAIL_ENABLED=bool, SMTP_LOGIN=(str, 'DEFAULT'))
        if env('MAIL_ENABLED'):
            ...
    """

    NOTSET = object()
    BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', '1')
    URL_CLASS = urlparse.ParseResult
    DATABASE_URL = 'DATABASE_URL'
    DB_SCHEMES = {
        'postgres': 'django.db.backends.postgresql_psycopg2',
        'postgresql': 'django.db.backends.postgresql_psycopg2',
        'postgis': 'django.contrib.gis.db.backends.postgis',
        'mysql': 'django.db.backends.mysql',
        'mysql2': 'django.db.backends.mysql',
        'sqlite': 'django.db.backends.sqlite3'
    }

    def __init__(self, **schema):
        self.schema = schema

    def __call__(self, var, cast=None, default=NOTSET):
        return self.get_value(var, cast=cast, default=default)

    # Shortcuts

    def str(self, var, default=NOTSET):
        """
        :rtype: str
        """
        return self.get_value(var, default=default)

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
        return self.get_value(var, cast=urlparse.urlparse, default=default)

    def db(self, var=DATABASE_URL, default=NOTSET, **kwargs):
        """
        :rtype: dict
        """
        return self.db_url_config(self.url(var, default=default), **kwargs)

    def path(self, var, default=NOTSET, **kwargs):
        """
        :rtype: Path
        """
        return Path(self.get_value(var, default=default), **kwargs)

    def get_value(self, var, cast=None, default=NOTSET):
        """Return value for given environment variable.

        :param var: Name of variable.
        :param cast: Type to cast return value as.
        :param default: If var not present in environ, return this instead.

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

        # Don't cast if we're returning a default value
        if value != default:
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
            value = map(cast[0], [x for x in value.split(',') if x])
        elif isinstance(cast, dict):
            key_cast = cast.get('key', str)
            value_cast = cast.get('value', str)
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
    def db_url_config(cls, url, **overrides):
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
        url = urlparse.urlparse(url) if not isinstance(url, cls.URL_CLASS) else url

        config = {}

        # Remove query strings.
        path = url.path[1:]
        path = path.split('?', 2)[0]

        # Update with environment configuration.
        config.update({
            'NAME': path,
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })

        # Update with kwargs configuration.
        config.update(overrides)

        if url.scheme in Env.DB_SCHEMES:
            config['ENGINE'] = Env.DB_SCHEMES[url.scheme]

        return config

    @staticmethod
    def read_env(env_file='.env', **overrides):
        """Pulled from Honcho code with minor updates, reads local default
        environment variables from a .env file located in the project root
        directory.

        http://www.wellfireinteractive.com/blog/easier-12-factor-django/

        https://gist.github.com/bennylope/2999704
        """
        logger.debug('Read environment variables from file: {0}'.format(env_file))
        try:
            with open(env_file) if isinstance(env_file, basestring) else env_file as f:
                content = f.read()
        except IOError:
            content = ''

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
                os.environ.setdefault(key, val)

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
        return Path(self.__root__, other if not isinstance(other, Path) else other.__root__[1:])

    def __sub__(self, other):
        if isinstance(other, int):
            return self.path('../' * other)
        raise TypeError("unsupported operand type(s) for -: 'str' and '{0}'".format(other.__class__.__name__))

    def __invert__(self):
        return self.path('..')

    def __contains__(self, item):
        base_path = self.__root__
        if len(base_path) > 1:
            base_path += '/'
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