====
Tips
====


Docker-style file based variables
=================================

To enable Docker-style file based variables (appended with ``_FILE``), use
``environ.FileAwareEnv`` rather than ``environ.Env``:

.. code-block:: python

    import environ

    env = environ.FileAwareEnv()

    # If a ``SECRET_KEY_FILE`` environment variable exists, its contents will be
    # read from the file system and used instead of the ``SECRET_KEY``
    # environment variable.
    SECRET_KEY = env('SECRET_KEY')


Using unsafe characters in URLs
===============================

In order to use unsafe characters you have to encode with ``urllib.parse.encode`` before you set into ``.env`` file.

.. code-block:: shell

   DATABASE_URL=mysql://user:%23password@127.0.0.1:3306/dbname

See https://perishablepress.com/stop-using-unsafe-characters-in-urls/ for reference.


Smart Casting
=============

``django-environ`` has a "Smart-casting" enabled by default, if you don't provide a ``cast`` type, it will be detected from ``default`` type.
This could raise side effects (see `#192 <https://github.com/joke2k/django-environ/issues/192>`_).
To disable it use ``env.smart_cast = False``.

.. note::

   The next major release will disable it by default.


Multiple redis cache locations
==============================

For redis cache, multiple master/slave or shard locations can be configured as follows:

.. code-block:: shell

   CACHE_URL='rediscache://master:6379,slave1:6379,slave2:6379/1'


Email settings
==============

In order to set email configuration for django you can use this code:

.. code-block:: python

   # The email() method is an alias for email_url().
   EMAIL_CONFIG = env.email(
       'EMAIL_URL',
       default='smtp://user:password@localhost:25'
   )

   vars().update(EMAIL_CONFIG)


SQLite urls
===========

SQLite connects to file based databases. The same URL format is used, omitting the hostname,
and using the "file" portion as the filename of the database.
This has the effect of four slashes being present for an absolute

file path: ``sqlite:////full/path/to/your/database/file.sqlite``.


Nested lists
============

Some settings such as Django's ``ADMINS`` make use of nested lists.
You can use something like this to handle similar cases.

.. code-block:: python

   # DJANGO_ADMINS=Blake:blake@cyb.org,Alice:alice@cyb.org
   ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS')]

   # or use more specific function

   from email.utils import getaddresses

   # DJANGO_ADMINS=Alice Judge <alice@cyb.org>,blake@cyb.org
   ADMINS = getaddresses([env('DJANGO_ADMINS')])

   # another option is to use parseaddr from email.utils

   # DJANGO_ADMINS="Blake <blake@cyb.org>, Alice Judge <alice@cyb.org>"
   from email.utils import parseaddr

   ADMINS = tuple(parseaddr(email) for email in env.list('DJANGO_ADMINS'))


Multiline value
===============

You can set a multiline variable value:

.. code-block:: python

   # MULTILINE_TEXT=Hello\\nWorld
   >>> print env.str('MULTILINE_TEXT', multiline=True)
   Hello
   World


Proxy value
===========

Values that being with a ``$`` may be interpolated. Pass ``interpolate=True`` to
``environ.Env()`` to enable this feature:

.. code-block:: python

   import environ

   env = environ.Env(interpolate=True)

   # BAR=FOO
   # PROXY=$BAR
   >>> print env.str('PROXY')
   FOO


.. _multiple-env-files-label:

Multiple env files
==================

There is an ability point to the .env file location using an environment
variable. This feature may be convenient in a production systems with a
different .env file location.

The following example demonstrates the above:

.. code-block:: shell

   # /etc/environment file contents
   DEBUG=False

.. code-block:: shell

   # .env file contents
   DEBUG=True

.. code-block:: python

   env = environ.Env()
   env.read_env(env.str('ENV_PATH', '.env'))


Now ``ENV_PATH=/etc/environment ./manage.py runserver`` uses ``/etc/environment``
while ``./manage.py runserver`` uses ``.env``.


Using Path objects when reading env
===================================

It is possible to use of ``pathlib.Path`` objects when reading environment file from the filesystem:

.. code-block:: python

   import os
   import pathlib

   import environ


   # Build paths inside the project like this: BASE_DIR('subdir').
   BASE_DIR = environ.Path(__file__) - 3

   env = environ.Env()

   # The four lines below do the same:
   env.read_env(BASE_DIR('.env'))
   env.read_env(os.path.join(BASE_DIR, '.env'))
   env.read_env(pathlib.Path(str(BASE_DIR)).joinpath('.env'))
   env.read_env(pathlib.Path(str(BASE_DIR)) / '.env')
