Changelog
=========

All notable changes to this project will be documented in this file.
The format is inspired by `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

`v0.9.0`_ - 00-Unreleased-2021
------------------------------

- WIP


`v0.8.1`_ - 20-October-2021
---------------------------
Fixed
+++++
- Fixed "Invalid line" spam logs on blank lines in env file
  `#340 <https://github.com/joke2k/django-environ/issues/340>`_.
- Fixed ``memcache``/``pymemcache`` URL parsing for correct identification of
  connection type `#337 <https://github.com/joke2k/django-environ/issues/337>`_.


`v0.8.0`_ - 17-October-2021
---------------------------
Added
+++++
- Log invalid lines when parse .env file
  `#283 <https://github.com/joke2k/django-environ/pull/283>`_.
- Added docker-style file variable support
  `#189 <https://github.com/joke2k/django-environ/issues/189>`_.
- Added option to override existing variables with ``read_env``
  `#103 <https://github.com/joke2k/django-environ/issues/103>`_,
  `#249 <https://github.com/joke2k/django-environ/issues/249>`_.
- Added support for empty var with None default value
  `#209 <https://github.com/joke2k/django-environ/issues/209>`_.
- Added ``pymemcache`` cache backend for Django 3.2+
  `#335 <https://github.com/joke2k/django-environ/pull/335>`_.


Fixed
+++++
- Keep newline/tab escapes in quoted strings
  `#296 <https://github.com/joke2k/django-environ/pull/296>`_.
- Handle escaped dollar sign in values
  `#271 <https://github.com/joke2k/django-environ/issues/271>`_.
- Fixed incorrect parsing of ``DATABASES_URL`` for Google Cloud MySQL
  `#294 <https://github.com/joke2k/django-environ/issues/294>`_.


`v0.7.0`_ - 11-September-2021
------------------------------
Added
+++++
- Added support for negative float strings
  `#160 <https://github.com/joke2k/django-environ/issues/160>`_.
- Added Elasticsearch5 to search scheme
  `#297 <https://github.com/joke2k/django-environ/pull/297>`_.
- Added Elasticsearch7 to search scheme
  `#314 <https://github.com/joke2k/django-environ/issues/314>`_.
- Added the ability to use ``bytes`` or ``str`` as a default value for ``Env.bytes()``.

Fixed
+++++
- Fixed links in the documentation.
- Use default option in ``Env.bytes()``
  `#206 <https://github.com/joke2k/django-environ/pull/206>`_.
- Safely evaluate a string containing an invalid Python literal
  `#200 <https://github.com/joke2k/django-environ/issues/200>`_.

Changed
+++++++
- Added 'Funding' and 'Say Thanks!' project urls on pypi.
- Stop raising ``UserWarning`` if ``.env`` file isn't found. Log a message with
  ``INFO`` log level instead `#243 <https://github.com/joke2k/django-environ/issues/243>`_.


`v0.6.0`_ - 4-September-2021
----------------------------
Added
+++++
- Python 3.9, 3.10 and pypy 3.7 are now supported.
- Django 3.1 and 3.2 are now supported.
- Added missed classifiers to ``setup.py``.
- Accept Python 3.6 path-like objects for ``read_env``
  `#106 <https://github.com/joke2k/django-environ/issues/106>`_,
  `#286 <https://github.com/joke2k/django-environ/issues/286>`_.

Fixed
+++++
- Fixed various code linting errors.
- Fixed typos in the documentation.
- Added missed files to the package contents.
- Fixed ``db_url_config`` to work the same for all postgres-like schemes
  `#264 <https://github.com/joke2k/django-environ/issues/264>`_,
  `#268 <https://github.com/joke2k/django-environ/issues/268>`_.

Changed
+++++++
- Refactor tests to use pytest and follow DRY.
- Moved CI to GitHub Actions.
- Restructuring of project documentation.
- Build and test package documentation as a part of CI pipeline.
- Build and test package distribution as a part of CI pipeline.
- Check ``MANIFEST.in`` in a source package for completeness as a part of CI
  pipeline.
- Added ``pytest`` and ``coverage[toml]`` to setuptools' ``extras_require``.


`v0.5.0`_ - 30-August-2021
--------------------------
Added
+++++
- Support for Django 2.1 & 2.2.
- Added tox.ini targets.
- Added secure redis backend URLs via ``rediss://``.
- Add ``cast=str`` to ``str()`` method.

Fixed
+++++
- Fixed misspelling in the documentation.

Changed
+++++++
- Validate empty cache url and invalid cache schema.
- Set ``long_description_content_type`` in setup.
- Improved Django 1.11 database configuration support.


`v0.4.5`_ - 25-June-2018
------------------------
Added
+++++
- Support for Django 2.0.
- Support for smart casting.
- Support PostgreSQL unix domain socket paths.
- Tip: Multiple env files.

Changed
+++++++
- Fix parsing option values ``None``, ``True`` and ``False``.
- Order of importance of engine configuration in ``db_url_config``.

Removed
+++++++
- Remove ``django`` and ``six`` dependencies.


`v0.4.4`_ - 21-August-2017
--------------------------

Added
+++++
- Support for ``django-redis`` multiple locations (master/slave, shards).
- Support for Elasticsearch2.
- Support for Mysql-connector.
- Support for ``pyodbc``.
- Add ``__contains__`` feature to Environ class.

Fixed
+++++
- Fix Path subtracting.


`v0.4.3`_ - 21-August-2017
--------------------------
Changed
+++++++
- Rollback the default Environ to ``os.environ``.

`v0.4.2`_ - 13-April-2017
-------------------------
Added
+++++
- Confirm support for Django 1.11.
- Support for Redshift database URL.

Changed
+++++++
- Fix uwsgi settings reload problem
  `#55 <https://github.com/joke2k/django-environ/issues/55>`_.
- Update support for ``django-redis`` urls
  `#109 <https://github.com/joke2k/django-environ/pull/109>`_.

`v0.4.1`_ - 13-November-2016
----------------------------
Added
+++++
- Add support for Django 1.10.

Changed
+++++++
- Fix for unsafe characters into URLs.
- Clarifying warning on missing or unreadable file.
  Thanks to `@nickcatal <https://github.com/nickcatal>`_.
- Fix support for Oracle urls.
- Fix support for ``django-redis``.

`v0.4`_ - 23-September-2015
---------------------------
Added
+++++
- New email schemes - ``smtp+ssl`` and ``smtp+tls`` (``smtps`` would be deprecated).
- Add tuple support. Thanks to `@anonymouzz <https://github.com/anonymouzz>`_.
- Add LDAP url support for database. Thanks to
  `django-ldapdb/django-ldapdb <https://github.com/django-ldapdb/django-ldapdb>`_.

Changed
+++++++
- Fix non-ascii values (broken in Python 2.x).
- ``redis_cache`` replaced by ``django_redis``.
- Fix psql/pgsql url.


`v0.3.1`_ - 19 Sep 2015
-----------------------
Added
+++++
- Added ``email`` as alias for ``email_url``.
- Django 1.7 is now supported.
- Added LDAP scheme support for ``db_url_config``.

Fixed
+++++
- Fixed typos in the documentation.
- Fixed ``environ.Path.__add__`` to correctly handle plus operator.
- Fixed ``environ.Path.__contains__`` to correctly work on Windows.


`v0.3`_ - 03-June-2014
----------------------
Added
+++++
- Add cache url support.
- Add email url support.
- Add search url support.

Changed
+++++++
- Rewriting README.rst.

v0.2.1 - 19-April-2013
----------------------
Changed
+++++++
- ``Env.__call__`` now uses ``Env.get_value`` instance method.

v0.2 - 16-April-2013
--------------------
Added
+++++
- Add advanced float parsing (comma and dot symbols to separate thousands and decimals).

Fixed
+++++
- Fixed typos in the documentation.

v0.1 - 2-April-2013
-------------------
Added
+++++
- Initial release.


.. _v0.9.0: https://github.com/joke2k/django-environ/compare/v0.8.1...develop
.. _v0.8.1: https://github.com/joke2k/django-environ/compare/v0.8.0...v0.8.1
.. _v0.8.0: https://github.com/joke2k/django-environ/compare/v0.7.0...v0.8.0
.. _v0.7.0: https://github.com/joke2k/django-environ/compare/v0.6.0...v0.7.0
.. _v0.6.0: https://github.com/joke2k/django-environ/compare/v0.5.0...v0.6.0
.. _v0.5.0: https://github.com/joke2k/django-environ/compare/v0.4.5...v0.5.0
.. _v0.4.5: https://github.com/joke2k/django-environ/compare/v0.4.4...v0.4.5
.. _v0.4.4: https://github.com/joke2k/django-environ/compare/v0.4.3...v0.4.4
.. _v0.4.3: https://github.com/joke2k/django-environ/compare/v0.4.2...v0.4.3
.. _v0.4.2: https://github.com/joke2k/django-environ/compare/v0.4.1...v0.4.2
.. _v0.4.1: https://github.com/joke2k/django-environ/compare/v0.4...v0.4.1
.. _v0.4: https://github.com/joke2k/django-environ/compare/v0.3.1...v0.4
.. _v0.3.1: https://github.com/joke2k/django-environ/compare/v0.3...v0.3.1
.. _v0.3: https://github.com/joke2k/django-environ/compare/v0.2.1...v0.3
