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

:py:class:`.environ.Env` may parse complex variables like ``BAR=key=val,foo=bar``
with the following type-casting ``BAR=(dict, {})``. For example:

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

:py:meth:`~.environ.Env.db_url` supports the following schemes:

* PostgreSQL: ``postgres://``, ``pgsql://``, ``psql://`` or ``postgresql://``
* PostGIS: ``postgis://``
* MySQL: ``mysql://`` or ``mysql2://``
* MySQL for GeoDjango: ``mysqlgis://``
* MySQL Connector Python from Oracle: ``mysql-connector://``
* SQLite: ``sqlite://``
* SQLite with SpatiaLite for GeoDjango: ``spatialite://``
* Oracle: ``oracle://``
* Microsoft SQL Server: ``mssql://``
* PyODBC: ``pyodbc://``
* Amazon Redshift: ``redshift://``
* LDAP: ``ldap://``


.. _environ-env-cache-url:

``environ.Env.cache_url``
=========================

:py:meth:`~.environ.Env.cache_url` supports the following schemes:

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

:py:meth:`~.environ.Env.search_url` supports the following schemes:

* Elasticsearch: ``elasticsearch://``
* Elasticsearch2: ``elasticsearch2://``
* Elasticsearch5: ``elasticsearch5://``
* Elasticsearch7: ``elasticsearch7://``
* Solr: ``solr://``
* Whoosh: ``whoosh://``
* Xapian: ``xapian://``
* Simple cache: ``simple://``


.. _environ-env-email-url:

``environ.Env.email_url``
==========================

:py:meth:`~.environ.Env.email_url` supports the following schemes:

* SMTP: ``smtp://``
* SMTP+SSL: ``smtp+ssl://``
* SMTP+TLS: ``smtp+tls://``
* Console mail: ``consolemail://``
* File mail: ``filemail://``
* LocMem mail: ``memorymail://``
* Dummy mail: ``dummymail://``
