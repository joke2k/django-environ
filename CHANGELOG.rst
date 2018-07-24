Changelog
=========
All notable changes to this project will be documented in this file.

The format is *inspired* by `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.


`v0.4.5`_ - 25-June-2018
--------------------------
Added
+++++
  - Support for Django 2.0
  - Support for smart casting
  - Support PostgreSQL unix domain socket paths
  - Tip: Multiple env files

Changed
+++++++
  - Fix parsing option values None, True and False
  - Order of importance of engine configuration in db_url_config

Removed
+++++++
  - Remove django and six dependencies


`v0.4.4`_ - 21-August-2017
--------------------------

Added
+++++
  - Support for django-redis multiple locations (master/slave, shards)
  - Support for Elasticsearch2
  - Support for Mysql-connector
  - Support for pyodbc
  - Add __contains__ feature to Environ class

Changed
+++++++
  - Fix Path subtracting


`v0.4.3`_ - 21-August-2017
--------------------------
Changed
+++++++
  - Rollback the default Environ to os.environ

`v0.4.2`_ - 13-April-2017
-------------------------
Added
+++++
  - Confirm support for Django 1.11.
  - Support for Redshift database URL

Changed
+++++++
  - Fix uwsgi settings reload problem (#55)
  - Update support for django-redis urls (#109)

`v0.4.1`_ - 13-November-2016
----------------------------
Added
+++++
  - Add support for Django 1.10

Changed
+++++++
  - Fix for unsafe characters into URLs
  - Clarifying warning on missing or unreadable file. Thanks to @nickcatal
  - Fix support for Oracle urls
  - Fix support for django-redis

`v0.4.0`_ - 23-September-2015
-----------------------------
Added
+++++
  - New email schemes - smtp+ssl and smtp+tls (smtps would be deprecated)
  - Add tuple support. Thanks to @anonymouzz
  - Add LDAP url support for database (django-ldapdb)

Changed
+++++++
  - Fix non-ascii values (broken in Python 2.x)
  - redis_cache replaced by django_redis
  - Fix psql/pgsql url

`v0.3`_ - 03-June-2014
----------------------
Added
+++++
  - Add cache url support
  - Add email url support
  - Add search url support

Changed
+++++++
  - Rewriting README.rst

0.2.1 19-April-2013
-------------------
Changed
+++++++
  - environ/environ.py: Env.__call__ now uses Env.get_value instance method

0.2 16-April-2013
-----------------
Changed
+++++++
  - environ/environ.py, environ/test.py, environ/test_env.txt: add advanced
    float parsing (comma and dot symbols to separate thousands and decimals)
  - README.rst, docs/index.rst: fix TYPO in documentation

0.1 2-April-2013
-----------------
Added
+++++
  - initial release


.. _v0.4.5: https://github.com/joke2k/django-environ/compare/v0.4.4...v0.4.5
.. _v0.4.4: https://github.com/joke2k/django-environ/compare/v0.4.3...v0.4.4
.. _v0.4.3: https://github.com/joke2k/django-environ/compare/v0.4.2...v0.4.3
.. _v0.4.2: https://github.com/joke2k/django-environ/compare/v0.4.1...v0.4.2
.. _v0.4.1: https://github.com/joke2k/django-environ/compare/v0.4.0...v0.4.1
.. _v0.4.0: https://github.com/joke2k/django-environ/compare/v0.3...v0.4.0
.. _v0.3: https://github.com/joke2k/django-environ/compare/v0.2.1...v0.3
.. _`Keep a Changelog`: http://keepachangelog.com/en/1.0.0/
.. _`Semantic Versioning`: http://semver.org/spec/v2.0.0.html
