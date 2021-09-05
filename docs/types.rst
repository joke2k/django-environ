===============
Supported types
===============

* ``str``
* ``bool``
* ``int``
* ``float``
* ``json``
* ``list``: ``(FOO=a,b,c)``
* ``tuple``: ``(FOO=(a,b,c))``
* ``dict``: ``(BAR=key=val,foo=bar)``, ``environ.Env(BAR=(dict, {}))``
* ``dict``: ``(BAR=key=val;foo=1.1;baz=True)``, ``environ.Env(BAR=(dict(value=unicode, cast=dict(foo=float,baz=bool)), {}))``
* ``url``
* ``path``: ``(environ.Path)``
* ``db_url``

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

* ``cache_url``

  * Database: ``dbcache://``
  * Dummy: ``dummycache://``
  * File: ``filecache://``
  * Memory: ``locmemcache://``
  * Memcached: ``memcache://``
  * Python memory: ``pymemcache://``
  * Redis: ``rediscache://``, ``redis://``, or ``rediss://``

* ``search_url``

  * Elasticsearch: ``elasticsearch://``
  * Elasticsearch2: ``elasticsearch2://``
  * Elasticsearch5: ``elasticsearch5://``
  * Solr: ``solr://``
  * Whoosh: ``whoosh://``
  * Xapian: ``xapian://``
  * Simple cache: ``simple://``

* ``email_url``

  * SMTP: ``smtp://``
  * SMTP+SSL: ``smtp+ssl://``
  * SMTP+TLS: ``smtp+tls://``
  * Console mail: ``consolemail://``
  * File mail: ``filemail://``
  * LocMem mail: ``memorymail://``
  * Dummy mail: ``dummymail://``
