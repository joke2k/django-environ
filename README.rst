Django-environ
==============

Django-environ allows you to utilize 12factor inspired environment variables to configure your Django application.

.. image:: https://travis-ci.org/joke2k/djang-environ.svg?branch=develop
  :target: https://travis-ci.org/joke2k/django-environ
.. image:: https://coveralls.io/repos/joke2k/django-environ/badge.png?branch=develop
  :target: https://coveralls.io/r/joke2k/django-environ?branch=develop
.. image:: https://badge.fury.io/py/django-environ.png
  :target: http://badge.fury.io/py/django-environ
.. image:: https://pypip.in/d/django-environ/badge.png
  :target: https://crate.io/packages/django-environ

This is your `settings.py` file before you have installed **django-environ**

::

    import os
    SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'database',
            'USER': 'user',
            'PASSWORD': 'githubbedpassword',
            'HOST': '127.0.0.1',
            'PORT': '8458',
        }
        'extra': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'database.sqlite')
        }
    }

    MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')
    MEDIA_URL = 'media/'
    STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
    STATIC_URL = 'static/'

    SECRET_KEY = '...im incredibly still here...'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '127.0.0.1:11211', '127.0.0.1:11212', '127.0.0.1:11213',
            ]
        },
        'redis': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '127.0.0.1:6379:1',
            'OPTIONS': {
                'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
                'PASSWORD': 'redis-githubbed-password',
            }
        }
    }

After::

    import environ
    root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
    env = environ.Env(DEBUG=(bool, False),) # set default values and casting

    SITE_ROOT = root()

    DEBUG = env('DEBUG') # False if not in os.environ
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
        'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
    }

    public_root = root.path('public/')

    MEDIA_ROOT = public_root('media')
    MEDIA_URL = 'media/'
    STATIC_ROOT = public_root('static')
    STATIC_URL = 'static/'

    SECRET_KEY = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ

    CACHES = {
        'default: env.cache(),
        'redis': env.cache('REDIS_URL')
    }

Create a `.env` file::

    DEBUG=on
    # DJANGO_SETTINGS_MODULE=myapp.settings.dev
    SECRET_KEY=your-secret-key
    DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
    # SQLITE_URL=sqlite:///my-local-sqlite.db
    CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
    REDIS_URL=rediscache://127.0.0.1:6379:1?client_class=redis_cache.client.DefaultClient&password=redis-un-githubbed-password

Open `manage.py` and `wsgi.py`. Add::

    import environ
    environ.Env.read_env()

You can also pass `read_env()` an explicit path to the .env file, or to the directory where it lives.

How to install
--------------

::

    $ pip install django-environ


How to use
----------

There are only classes, Env and Path

::

    >>> import environ
    >>> env = environ.Env(
            DEBUG=(bool, False),
        )
    >>> env('DEBUG')
    False
    >>> env('DEBUG', default=True)
    True

    >>> open('.myenv', 'a').write('DEBUG=on')
    >>> environ.Env.read_env('.`myenv') # or env.read_env('.myenv')
    >>> env('DEBUG')
    True

    >>> open('.myenv', 'a').write('\nINT_VAR=1010')
    >>> env.int('INT_VAR'), env.str('INT_VAR')
    1010, '1010'

    >>> open('.myenv', 'a').write('\nDATABASE_URL=sqlite:///my-local-sqlite.db')
    >>> env.read_env('.myenv')
    >>> env.db()
    {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'my-local-sqlite.db', 'HOST': '', 'USER': '', 'PASSWORD': '', 'PORT': ''}

    >>> root = env.path('/home/myproject/')
    >>> root('static')
    '/home/myproject/static'


Supported Types
---------------

- str
- bool
- int
- float
- json
- list (FOO=a,b,c)
- dict (BAR=key=val;foo=bar)
- url
- db
    -  PostgreSQL: postgres://, pgsql:// or postgresql://
    -  PostGIS: postgis://
    -  MySQL: mysql:// or mysql2://
    -  MySQL for GeoDjango: mysqlgis://
    -  SQLITE: sqlite://
    -  SQLITE with SPATIALITE for GeoDjango: spatialite://

- cache (see Supported Caches)
    -  Database: dbcache://
    -  Dummy: dummycache://
    -  File: filecache://
    -  Memory: locmemcache://
    -  Memcached: memcache://
    -  Python memory: pymemcache://
    -  Redis: rediscache://

- path (environ.Path)

Tests
-----

::

    $ git clone git@github.com:joke2k/django-environ.git
    $ cd django-environ/
    $ python setup.py test


Changelog
---------

=== 0.3.0 (2014-06-??) ===

  * Add cache url support
  * Add email url support
  * Rewriting README.rst


=== 0.2.1 (2013-04-19) ===

  * environ/environ.py: Env.__call__ now uses Env.get_value instance method

=== 0.2 (2013-04-16) ===

  * environ/environ.py, environ/test.py, environ/test_env.txt: add advanced
    float parsing (comma and dot symbols to separate thousands and decimals)

  * README.rst, docs/index.rst: fix TYPO in documentation

=== 0.1 (2013-04-02) ===

  * initial release

Credits
-------

- `12factor`_
- `12factor-django`_
- `Two Scoops of Django`_
- `rconradharris`_ / `envparse`_
- `kennethreitz`_ / `dj-database-url`_
- `migonzalvar`_ / `dj-email-url`_
- `ghickman`_ / `dj-cache-url`_
- `julianwachholz`_ / `dj-config-url`_
- `nickstenning`_ / `honcho`_
- `envparse`_
- `Distribute`_
- `modern-package-template`_

.. _rconradharris: https://github.com/rconradharris
.. _envparse: https://github.com/rconradharris/envparse

.. _kennethreitz: https://github.com/kennethreitz
.. _dj-database-url: https://github.com/kennethreitz/dj-database-url

.. _migonzalvar: https://github.com/migonzalvar
.. _dj-email-url: https://github.com/migonzalvar/dj-email-url

.. _ghickman: https://github.com/ghickman
.. _dj-cache-url: https://github.com/ghickman/django-cache-url

.. _julianwachholz: https://github.com/julianwachholz
.. _dj-config-url: https://github.com/julianwachholz/dj-config-url

.. _nickstenning: https://github.com/nickstenning
.. _honcho: https://github.com/nickstenning/honcho

.. _12factor: http://www.12factor.net/
.. _12factor-django: http://www.wellfireinteractive.com/blog/easier-12-factor-django/
.. _`Two Scoops of Django`: https://django.2scoops.org (book)


.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
