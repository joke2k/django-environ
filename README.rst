==============
Django-environ
==============

Django-environ allows you to utilize 12factor inspired environment variables to configure your Django application.

|pypi| |unix_build| |windows_build| |coverage| |license|


This module is a merge of:

* `envparse`_
* `honcho`_
* `dj-database-url`_
* `dj-search-url`_
* `dj-config-url`_
* `django-cache-url`_

and inspired by:

* `12factor`_
* `12factor-django`_
* `Two Scoops of Django`_

This is your `settings.py` file before you have installed **django-environ**

.. code-block:: python

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
        },
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
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': '127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PASSWORD': 'redis-githubbed-password',
            }
        }
    }

After:

.. code-block:: python

    import environ
    root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
    env = environ.Env(DEBUG=(bool, False),) # set default values and casting
    environ.Env.read_env() # reading .env file

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
        'default': env.cache(),
        'redis': env.cache('REDIS_URL')
    }

You can also pass ``read_env()`` an explicit path to the ``.env`` file.

Create a ``.env`` file:

.. code-block:: bash

    DEBUG=on
    # DJANGO_SETTINGS_MODULE=myapp.settings.dev
    SECRET_KEY=your-secret-key
    DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
    # SQLITE_URL=sqlite:///my-local-sqlite.db
    CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
    REDIS_URL=rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password=redis-un-githubbed-password


How to install
==============

::

    $ pip install django-environ


How to use
==========

There are only two classes, ``environ.Env`` and ``environ.Path``

.. code-block:: python

    >>> import environ
    >>> env = environ.Env(
            DEBUG=(bool, False),
        )
    >>> env('DEBUG')
    False
    >>> env('DEBUG', default=True)
    True

    >>> open('.myenv', 'a').write('DEBUG=on')
    >>> environ.Env.read_env('.myenv') # or env.read_env('.myenv')
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


See `cookiecutter-django`_ for a concrete example on using with a django project.


Supported Types
===============

- str
- bool
- int
- float
- json
- list (FOO=a,b,c)
- tuple (FOO=(a,b,c))
- dict (BAR=key=val,foo=bar) #environ.Env(BAR=(dict, {}))
- dict (BAR=key=val;foo=1.1;baz=True) #environ.Env(BAR=(dict(value=unicode, cast=dict(foo=float,baz=bool)), {}))
- url
- path (environ.Path)
- db_url
    -  PostgreSQL: postgres://, pgsql://, psql:// or postgresql://
    -  PostGIS: postgis://
    -  MySQL: mysql:// or mysql2://
    -  MySQL for GeoDjango: mysqlgis://
    -  SQLITE: sqlite://
    -  SQLITE with SPATIALITE for GeoDjango: spatialite://
    -  Oracle: oracle://
    -  PyODBC: pyodbc://
    -  Redshift: redshift://
    -  LDAP: ldap://
- cache_url
    -  Database: dbcache://
    -  Dummy: dummycache://
    -  File: filecache://
    -  Memory: locmemcache://
    -  Memcached: memcache://
    -  Python memory: pymemcache://
    -  Redis: rediscache://
- search_url
    - ElasticSearch: elasticsearch://
    - Solr: solr://
    - Whoosh: whoosh://
    - Xapian: xapian://
    - Simple cache: simple://
- email_url
    - SMTP: smtp://
    - SMTP+SSL: smtp+ssl://
    - SMTP+TLS: smtp+tls://
    - Console mail: consolemail://
    - File mail: filemail://
    - LocMem mail: memorymail://
    - Dummy mail: dummymail://

Tips
====

Using unsafe characters in URLs
-------------------------------

In order to use unsafe characters you have to encode with ``urllib.parse.encode`` before you set into ``.env`` file.

.. code-block::

    DATABASE_URL=mysql://user:%23password@127.0.0.1:3306/dbname


See https://perishablepress.com/stop-using-unsafe-characters-in-urls/ for reference.

Multiple redis cache locations
------------------------------

For redis cache, `multiple master/slave or shard locations <http://niwinz.github.io/django-redis/latest/#_pluggable_clients>`_ can be configured as follows:

.. code-block::

    CACHE_URL='rediscache://master:6379,slave1:6379,slave2:6379/1'

Email settings
--------------

In order to set email configuration for django you can use this code:

.. code-block:: python

    EMAIL_CONFIG = env.email_url(
        'EMAIL_URL', default='smtp://user@:password@localhost:25')

    vars().update(EMAIL_CONFIG)


SQLite urls
-----------

SQLite connects to file based databases. The same URL format is used, omitting the hostname,
and using the "file" portion as the filename of the database.
This has the effect of four slashes being present for an absolute
file path: sqlite:////full/path/to/your/database/file.sqlite.


Tests
=====

::

    $ git clone git@github.com:joke2k/django-environ.git
    $ cd django-environ/
    $ python setup.py test


License
=======

Django-environ is licensed under the MIT License - see the `LICENSE_FILE`_ file for details

Changelog
=========


`0.4.4 - 21-August-2017 <https://github.com/joke2k/django-environ/compare/v0.4.3...v0.4.4>`__
---------------------------------------------------------------------------------------------

  - Support for django-redis multiple locations (master/slave, shards)
  - Support for Elasticsearch2
  - Support for Mysql-connector
  - Support for pyodbc
  - Add __contains__ feature to Environ class
  - Fix Path subtracting


`0.4.3 - 21-August-2017 <https://github.com/joke2k/django-environ/compare/v0.4.2...v0.4.3>`__
---------------------------------------------------------------------------------------------

  - Rollback the default Environ to os.environ

`0.4.2 - 13-April-2017 <https://github.com/joke2k/django-environ/compare/v0.4.1...v0.4.2>`__
--------------------------------------------------------------------------------------------

  - Confirm support for Django 1.11.
  - Support for Redshift database URL
  - Fix uwsgi settings reload problem (#55)
  - Update support for django-redis urls (#109)

`0.4.1 - 13-November-2016 <https://github.com/joke2k/django-environ/compare/v0.4...v0.4.1>`__
---------------------------------------------------------------------------------------------
  - Fix for unsafe characters into URLs
  - Clarifying warning on missing or unreadable file. Thanks to @nickcatal
  - Add support for Django 1.10.
  - Fix support for Oracle urls
  - Fix support for django-redis


`0.4.0 - 23-September-2015 <https://github.com/joke2k/django-environ/compare/v0.3...v0.4>`__
--------------------------------------------------------------------------------------------
  - Fix non-ascii values (broken in Python 2.x)
  - New email schemes - smtp+ssl and smtp+tls (smtps would be deprecated)
  - redis_cache replaced by django_redis
  - Add tuple support. Thanks to @anonymouzz
  - Add LDAP url support for database (django-ldapdb)
  - Fix psql/pgsql url

`0.3 - 03-June-2014 <https://github.com/joke2k/django-environ/compare/v0.2.1...v0.3>`__
---------------------------------------------------------------------------------------
  - Add cache url support
  - Add email url support
  - Add search url support
  - Rewriting README.rst

0.2.1 19-April-2013
-------------------
  - environ/environ.py: Env.__call__ now uses Env.get_value instance method

0.2 16-April-2013
-----------------
  - environ/environ.py, environ/test.py, environ/test_env.txt: add advanced
    float parsing (comma and dot symbols to separate thousands and decimals)
  - README.rst, docs/index.rst: fix TYPO in documentation

0.1 02-April-2013
-----------------
  - initial release

Credits
=======

- `12factor`_
- `12factor-django`_
- `Two Scoops of Django`_
- `rconradharris`_ / `envparse`_
- `kennethreitz`_ / `dj-database-url`_
- `migonzalvar`_ / `dj-email-url`_
- `ghickman`_ / `django-cache-url`_
- `dstufft`_ / `dj-search-url`_
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
.. _django-cache-url: https://github.com/ghickman/django-cache-url

.. _julianwachholz: https://github.com/julianwachholz
.. _dj-config-url: https://github.com/julianwachholz/dj-config-url

.. _dstufft: https://github.com/dstufft
.. _dj-search-url: https://github.com/dstufft/dj-search-url

.. _nickstenning: https://github.com/nickstenning
.. _honcho: https://github.com/nickstenning/honcho

.. _12factor: http://www.12factor.net/
.. _12factor-django: http://www.wellfireinteractive.com/blog/easier-12-factor-django/
.. _`Two Scoops of Django`: http://twoscoopspress.org/

.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template

.. _cookiecutter-django: https://github.com/pydanny/cookiecutter-django

.. |pypi| image:: https://img.shields.io/pypi/v/django-environ.svg?style=flat-square&label=version
    :target: https://pypi.python.org/pypi/django-environ
    :alt: Latest version released on PyPi

.. |coverage| image:: https://img.shields.io/coveralls/joke2k/django-environ/master.svg?style=flat-square
    :target: https://coveralls.io/r/joke2k/django-environ?branch=master
    :alt: Test coverage

.. |unix_build| image:: https://img.shields.io/travis/joke2k/django-environ/master.svg?style=flat-square&label=unix%20build
    :target: http://travis-ci.org/joke2k/django-environ
    :alt: Build status of the master branch on Mac/Linux

.. |windows_build|  image:: https://img.shields.io/appveyor/ci/joke2k/django-environ.svg?style=flat-square&label=windows%20build
    :target: https://ci.appveyor.com/project/joke2k/django-environ
    :alt: Build status of the master branch on Windows

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://raw.githubusercontent.com/joke2k/django-environ/master/LICENSE.txt
    :alt: Package license

.. _LICENSE_FILE: https://github.com/joke2k/django-environ/blob/master/LICENSE.txt
