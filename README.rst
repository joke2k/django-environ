.. raw:: html

    <h1 align="center">django-environ</h1>
    <p align="center">
        <a href="https://pypi.python.org/pypi/django-environ">
            <img src="https://img.shields.io/pypi/v/django-environ.svg" alt="Latest version released on PyPi" />
        </a>
        <a href="https://coveralls.io/github/joke2k/django-environ">
            <img src="https://coveralls.io/repos/github/joke2k/django-environ/badge.svg" alt="Coverage Status" />
        </a>
        <a href="https://github.com/joke2k/django-environ/actions?workflow=CI">
            <img src="https://github.com/joke2k/django-environ/workflows/CI/badge.svg?branch=develop" alt="CI Status" />
        </a>
        <a href="https://opencollective.com/django-environ">
            <img src="https://opencollective.com/django-environ/sponsors/badge.svg" alt="Sponsors on Open Collective" />
        </a>
        <a href="https://opencollective.com/django-environ">
            <img src="https://opencollective.com/django-environ/backers/badge.svg" alt="Backers on Open Collective" />
        </a>
        <a href="https://saythanks.io/to/joke2k">
            <img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg" alt="Say Thanks!" />
        </a>
        <a href="https://raw.githubusercontent.com/joke2k/django-environ/main/LICENSE.txt">
            <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="Package license" />
        </a>
    </p>

.. -teaser-begin-

**django-environ** is the Python package that allows you to use
`Twelve-factor methodology`_ to configure your Django application with
environment variables.

.. -teaser-end-

|cover|

.. _settings.py:

.. code-block:: python

    import environ
    env = environ.Env(
        # set casting, default value
        DEBUG=(bool, False)
    )
    # reading .env file
    environ.Env.read_env()

    # False if not in os.environ
    DEBUG = env('DEBUG')

    # Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
    SECRET_KEY = env('SECRET_KEY')

    # Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
    DATABASES = {
        # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
        'default': env.db(),
        # read os.environ['SQLITE_URL']
        'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
    }

    CACHES = {
        # read os.environ['CACHE_URL'] and raises ImproperlyConfigured exception if not found
        'default': env.cache(),
        # read os.environ['REDIS_URL']
        'redis': env.cache('REDIS_URL')
    }

See the `similar code, without django-environ <https://gist.github.com/joke2k/cc30ed2d5ccda52d5b551ccbc17e536b>`_.

::

         _ _                                              _
        | (_)                                            (_)
      __| |_  __ _ _ __   __ _  ___ ______ ___ _ ____   ___ _ __ ___  _ __
     / _` | |/ _` | '_ \ / _` |/ _ \______/ _ \ '_ \ \ / / | '__/ _ \| '_ \
    | (_| | | (_| | | | | (_| | (_) |    |  __/ | | \ V /| | | | (_) | | | |
     \__,_| |\__,_|_| |_|\__, |\___/      \___|_| |_|\_/ |_|_|  \___/|_| |_|
         _/ |             __/ |
        |__/             |___/


The idea of this package is to unify a lot of packages that make the same stuff:
Take a string from ``os.environ``, parse and cast it to some of useful python typed variables.
To do that and to use the `12factor`_ approach, some connection strings are expressed as url,
so this package can parse it and return a ``urllib.parse.ParseResult``.
These strings from ``os.environ`` are loaded from a `.env` file and filled in ``os.environ`` with ``setdefault`` method,
to avoid to overwrite the real environ.
A similar approach is used in `Two Scoops of Django`_ book and explained in `12factor-django`_ article.

Using django-environ you can stop to make a lot of unversioned ``settings_*.py`` to configure your app.
See `cookiecutter-django`_ for a concrete example on using with a django project.

Feature Support
---------------
- Fast and easy multi environment for deploy
- Fill ``os.environ`` with .env file variables
- Variables casting (see supported_types_ below)
- Url variables exploded to django specific package settings

Django-environ officially supports Django 1.11, 2.2 and 3.0.


Installation
------------

.. code-block:: bash

    $ pip install django-environ

*NOTE: No need to add it to INSTALLED_APPS.*


Then create a ``.env`` file:

.. code-block:: bash

    DEBUG=on
    SECRET_KEY=your-secret-key
    DATABASE_URL=psql://user:un-githubbedpassword@127.0.0.1:8458/database
    SQLITE_URL=sqlite:///my-local-sqlite.db
    CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
    REDIS_URL=rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password=ungithubbed-secret

And use it with `settings.py`_ above.
Don't forget to add ``.env`` in your ``.gitignore`` (tip: add ``.env.example`` with a template of your variables).

Documentation
-------------

Documentation is available at `RTFD <http://django-environ.rtfd.io/>`_.

.. _supported_types:

Supported types
---------------

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
    -  Mysql Connector Python from Oracle: mysql-connector://
    -  SQLITE: sqlite://
    -  SQLITE with SPATIALITE for GeoDjango: spatialite://
    -  Oracle: oracle://
    -  MSSQL: mssql://
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
    -  Redis: rediscache://, redis://, or rediss://
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
----

Using unsafe characters in URLs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to use unsafe characters you have to encode with ``urllib.parse.encode`` before you set into ``.env`` file.

.. code-block:: bash

    DATABASE_URL=mysql://user:%23password@127.0.0.1:3306/dbname

See https://perishablepress.com/stop-using-unsafe-characters-in-urls/ for reference.

Smart Casting
~~~~~~~~~~~~~

django-environ has a "Smart-casting" enabled by default, if you don't provide a ``cast`` type, it will be detected from ``default`` type.
This could raise side effects (see `#192 <https://github.com/joke2k/django-environ/issues/192>`_).
To disable it use ``env.smart_caset = False``.
New major release will disable it as default. 


Multiple redis cache locations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For redis cache, `multiple master/slave or shard locations <http://niwinz.github.io/django-redis/latest/#_pluggable_clients>`_ can be configured as follows:

.. code-block:: bash

    CACHE_URL='rediscache://master:6379,slave1:6379,slave2:6379/1'

Email settings
~~~~~~~~~~~~~~

In order to set email configuration for django you can use this code:

.. code-block:: python

    EMAIL_CONFIG = env.email_url(
        'EMAIL_URL', default='smtp://user:password@localhost:25')

    vars().update(EMAIL_CONFIG)

SQLite urls
~~~~~~~~~~~

SQLite connects to file based databases. The same URL format is used, omitting the hostname,
and using the "file" portion as the filename of the database.
This has the effect of four slashes being present for an absolute

file path: ``sqlite:////full/path/to/your/database/file.sqlite``.

Nested lists
------------

Some settings such as Django's ``ADMINS`` make use of nested lists. You can use something like this to handle similar cases.

.. code-block:: python

    # DJANGO_ADMINS=John:john@admin.com,Jane:jane@admin.com
    ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS')]

    # or use more specific function

    from email.utils import getaddresses

    # DJANGO_ADMINS=Full Name <email-with-name@example.com>,anotheremailwithoutname@example.com
    ADMINS = getaddresses([env('DJANGO_ADMINS')])

Multiline value
---------------

You can set a multiline variable value:

.. code-block:: python

    # MULTILINE_TEXT=Hello\\nWorld
    >>> print env.str('MULTILINE_TEXT', multiline=True)
    Hello
    World


Proxy value
-----------

You can set a value prefixed by ``$`` to use as a proxy to another variable value:

.. code-block:: python

    # BAR=FOO
    # PROXY=$BAR
    >>> print env.str('PROXY')
    FOO

Multiple env files
------------------
It is possible to have multiple env files and select one using environment variables.

.. code-block:: python

    env = environ.Env()
    env.read_env(env.str('ENV_PATH', '.env'))

Now ``ENV_PATH=other-env ./manage.py runserver`` uses ``other-env`` while ``./manage.py runserver`` uses ``.env``.

Tests
=====

::

    $ git clone git@github.com:joke2k/django-environ.git
    $ cd django-environ/
    $ python setup.py test

How to Contribute
-----------------
#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a `Contributor Friendly`_ tag for issues that should be ideal for people who are not very familiar with the codebase yet.
#. Fork `the repository`_ on GitHub to start making your changes to the **develop** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to `Authors file`_.

License
-------

This project is licensed under the MIT License - see the `License file`_ file for details

Changelog
---------

See the `Changelog file`_ which format is *inspired* by `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_.

Credits
-------
- See `Authors file`_
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
- `rconradharris`_ / `envparse`_
- `Distribute`_
- `modern-package-template`_

Contributors
-----------------
Thank you to all the people who have already contributed. 
|occontributorimage|

Backers
-----------------
Thank you to all our backers! 
|ocbackerimage|

Sponsors
-----------------
Support this project by becoming a sponsor. Your logo will show up here with a link to your website. `Became sponsor`_.

|ocsponsor0| |ocsponsor1| |ocsponsor2|

.. _rconradharris: https://github.com/rconradharris
.. _envparse: https://github.com/rconradharris/envparse

.. _jacobian: https://github.com/jacobian
.. _dj-database-url: https://github.com/jacobian/dj-database-url

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
.. _`Twelve-factor methodology`: http://www.12factor.net/
.. _12factor-django: http://www.wellfireinteractive.com/blog/easier-12-factor-django/
.. _`Two Scoops of Django`: http://twoscoopspress.org/

.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template

.. _cookiecutter-django: https://github.com/pydanny/cookiecutter-django

.. |cover| image:: https://farm2.staticflickr.com/1745/42580036751_35f76a92fe_h.jpg
    :alt: Photo by Singkham from Pexels

.. _`License file`: https://github.com/joke2k/django-environ/blob/develop/LICENSE.txt
.. _`Changelog file`: https://github.com/joke2k/django-environ/blob/develop/CHANGELOG.rst
.. _`Authors file`: https://github.com/joke2k/django-environ/blob/develop/AUTHORS.rst
.. _`Contributor Friendly`: https://github.com/joke2k/django-environ/issues?direction=desc&labels=contributor-friendly&page=1&sort=updated&state=open
.. _`the repository`: https://github.com/joke2k/django-environ
    
.. |ocbackerimage| image:: https://opencollective.com/django-environ/backers.svg?width=890
    :target: https://opencollective.com/django-environ
    :alt: Backers on Open Collective
.. |occontributorimage| image:: https://opencollective.com/django-environ/contributors.svg?width=890&button=false
    :target: https://opencollective.com/django-environ
    :alt: Repo Contributors

.. _`Became sponsor`: https://opencollective.com/django-environ#sponsor

.. |ocsponsor0| image:: https://opencollective.com/django-environ/sponsor/0/avatar.svg
    :target: https://opencollective.com/django-environ/sponsor/0/website
    :alt: Sponsor
.. |ocsponsor1| image:: https://opencollective.com/django-environ/sponsor/1/avatar.svg
    :target: https://opencollective.com/django-environ/sponsor/1/website
    :alt: Sponsor
.. |ocsponsor2| image:: https://opencollective.com/django-environ/sponsor/2/avatar.svg
    :target: https://opencollective.com/django-environ/sponsor/2/website
    :alt: Sponsor
