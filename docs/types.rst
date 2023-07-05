===============
Supported types
===============

The following are all type-casting methods of :py:class:`.environ.Env`.

* :py:meth:`~.environ.Env.str`
* :py:meth:`~.environ.Env.bool`
* :py:meth:`~.environ.Env.int`
* :py:meth:`~.environ.Env.float`
* :py:meth:`~.environ.Env.json`
* :py:meth:`~.environ.Env.url`
* :py:meth:`~.environ.Env.list`: (accepts values like ``(FOO=a,b,c)``)
* :py:meth:`~.environ.Env.tuple`:  (accepts values like ``(FOO=(a,b,c))``)
* :py:meth:`~.environ.Env.path`:  (accepts values like ``(environ.Path)``)
* :py:meth:`~.environ.Env.dict`:   (see below, ":ref:`environ-env-dict`" section)
* :py:meth:`~.environ.Env.db_url` (see below, ":ref:`environ-env-db-url`" section)
* :py:meth:`~.environ.Env.cache_url` (see below, ":ref:`environ-env-cache-url`" section)
* :py:meth:`~.environ.Env.search_url` (see below, ":ref:`environ-env-search-url`" section)
* :py:meth:`~.environ.Env.email_url` (see below, ":ref:`environ-env-email-url`" section)


.. _environ-env-dict:

``environ.Env.dict``
======================

:py:class:`.environ.Env` may parse complex variables like with the complex type-casting.
For example:

.. code-block:: python

   import environ


   env = environ.Env()

   # {'key': 'val', 'foo': 'bar'}
   env.parse_value('key=val,foo=bar', dict)

   # {'key': 'val', 'foo': 1.1, 'baz': True}
   env.parse_value(
       'key=val;foo=1.1;baz=True',
       dict(value=str, cast=dict(foo=float,baz=bool))
  )

For more detailed example see ":ref:`complex_dict_format`".


.. _environ-env-db-url:

``environ.Env.db_url``
======================

:py:meth:`~.environ.Env.db_url` supports the following URL schemas:

.. glossary::

    Amazon Redshift
      **Database Backend:** ``django_redshift_backend``

      **URL schema:** ``redshift://``

    LDAP
      **Database Backend:** ``ldapdb.backends.ldap``

      **URL schema:** ``ldap://host:port/dn?attrs?scope?filter?exts``

    MSSQL
      **Database Backend:** ``sql_server.pyodbc``

      **URL schema:** ``mssql://user:password@host:port/dbname``

      With MySQL you can use the following schemas: ``mysql``, ``mysql2``.

    MySQL (GIS)
      **Database Backend:** ``django.contrib.gis.db.backends.mysql``

      **URL schema:** ``mysqlgis://user:password@host:port/dbname``

    MySQL
      **Database Backend:** ``django.db.backends.mysql``

      **URL schema:** ``mysql://user:password@host:port/dbname``

    MySQL Connector Python from Oracle
      **Database Backend:** ``mysql.connector.django``

      **URL schema:** ``mysql-connector://``

    Oracle
      **Database Backend:** ``django.db.backends.oracle``

      **URL schema:** ``oracle://user:password@host:port/dbname``

    PostgreSQL
      **Database Backend:** ``django.db.backends.postgresql``

      **URL schema:** ``postgres://user:password@host:port/dbname``

      With PostgreSQL you can use the following schemas: ``postgres``, ``postgresql``, ``psql``, ``pgsql``, ``postgis``.
      You can also use UNIX domain sockets path instead of hostname. For example: ``postgres://path/dbname``.
      The ``django.db.backends.postgresql_psycopg2`` will be used if the Django version is less than ``2.0``.

    PostGIS
      **Database Backend:** ``django.contrib.gis.db.backends.postgis``

      **URL schema:** ``postgis://user:password@host:port/dbname``

    PyODBC
      **Database Backend:** ``sql_server.pyodbc``

      **URL schema:** ``pyodbc://``

    SQLite
      **Database Backend:** ``django.db.backends.sqlite3``

      **URL schema:** ``sqlite:////absolute/path/to/db/file``

      SQLite connects to file based databases. URL schemas ``sqlite://`` or
      ``sqlite://:memory:`` means the database is in the memory (not a file on disk).

    SpatiaLite
      **Database Backend:** ``django.contrib.gis.db.backends.spatialite``

      **URL schema:** ``spatialite:///PATH``

      SQLite connects to file based databases. URL schemas ``sqlite://`` or
      ``sqlite://:memory:`` means the database is in the memory (not a file on disk).


.. _environ-env-cache-url:

``environ.Env.cache_url``
=========================

:py:meth:`~.environ.Env.cache_url` supports the following URL schemas:

* Database: ``dbcache://``
* Dummy: ``dummycache://``
* File: ``filecache://``
* Memory: ``locmemcache://``
* Memcached:

  * ``memcache://`` (uses ``python-memcached`` backend, deprecated in Django 3.2)
  * ``pymemcache://`` (uses ``pymemcache`` backend if Django >=3.2 and package is installed, otherwise will use ``pylibmc`` backend to keep config backwards compatibility)
  * ``pylibmc://``

* Redis: ``rediscache://``, ``redis://``, or ``rediss://``


.. _environ-env-search-url:

``environ.Env.search_url``
==========================

:py:meth:`~.environ.Env.search_url` supports the following URL schemas:

* Elasticsearch: ``elasticsearch://`` (http) or ``elasticsearchs://`` (https)
* Elasticsearch2: ``elasticsearch2://`` (http) or ``elasticsearch2s://`` (https)
* Elasticsearch5: ``elasticsearch5://`` (http) or ``elasticsearch5s://`` (https)
* Elasticsearch7: ``elasticsearch7://`` (http) or ``elasticsearch7s://`` (https)
* Solr: ``solr://``
* Whoosh: ``whoosh://``
* Xapian: ``xapian://``
* Simple cache: ``simple://``


.. _environ-env-email-url:

``environ.Env.email_url``
==========================

:py:meth:`~.environ.Env.email_url` supports the following URL schemas:

* SMTP: ``smtp://``
* SMTP+SSL: ``smtp+ssl://``
* SMTP+TLS: ``smtp+tls://``
* Console mail: ``consolemail://``
* File mail: ``filemail://``
* LocMem mail: ``memorymail://``
* Dummy mail: ``dummymail://``
