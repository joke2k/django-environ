====
Tips
====


Docker-style file based variables
=================================

Docker (swarm) and Kubernetes are two widely used platforms that store their
secrets in tmpfs inside containers as individual files, providing a secure way
to be able to share configuration data between containers.

Use :class:`.environ.FileAwareEnv` rather than :class:`.environ.Env` to first look for
environment variables with ``_FILE`` appended. If found, their contents will be
read from the file system and used instead.

For example, given an app with the following in its settings module:

.. code-block:: python

   import environ

   env = environ.FileAwareEnv()
   SECRET_KEY = env("SECRET_KEY")

the example ``docker-compose.yml`` for would contain:

.. code-block:: yaml

   secrets:
     secret_key:
       external: true

   services:
     app:
       secrets:
         - secret_key
       environment:
         - SECRET_KEY_FILE=/run/secrets/secret_key


Using unsafe characters in URLs
===============================

In order to use unsafe characters you have to encode with :py:func:`urllib.parse.quote`
before you set into ``.env`` file. Encode only the value (i.e. the password) not the whole url.

.. code-block:: shell

   DATABASE_URL=mysql://user:%23password@127.0.0.1:3306/dbname

See https://perishablepress.com/stop-using-unsafe-characters-in-urls/ for reference.


Smart Casting
=============

django-environ has a "Smart-casting" enabled by default, if you don't provide a ``cast`` type, it will be detected from ``default`` type.
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

In order to set email configuration for Django you can use this code:

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


.. _complex_dict_format:

Complex dict format
===================

Sometimes we need to get a bit more complex dict type than usual. For example,
consider Djangosaml2's ``SAML_ATTRIBUTE_MAPPING``:

.. code-block:: python

   SAML_ATTRIBUTE_MAPPING = {
       'uid': ('username', ),
       'mail': ('email', ),
       'cn': ('first_name', ),
       'sn': ('last_name', ),
   }

A dict of this format can be obtained as shown below:

**.env file**:

.. code-block:: shell

   # .env file contents
   SAML_ATTRIBUTE_MAPPING="uid=username;mail=email;cn=first_name;sn=last_name;"

**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ


   env = environ.Env()

   # {'uid': ('username',), 'mail': ('email',), 'cn': ('first_name',), 'sn': ('last_name',)}
   SAML_ATTRIBUTE_MAPPING = env.dict(
       'SAML_ATTRIBUTE_MAPPING',
       cast={'value': tuple},
       default={}
   )


Multiline value
===============

To get multiline value pass ``multiline=True`` to ```str()```.

.. note::

   You shouldn't escape newline/tab characters yourself if you want to preserve
   the formatting.

The following example demonstrates the above:

**.env file**:

.. code-block:: shell

   # .env file contents
   UNQUOTED_CERT=---BEGIN---\r\n---END---
   QUOTED_CERT="---BEGIN---\r\n---END---"
   ESCAPED_CERT=---BEGIN---\\n---END---

**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ


   env = environ.Env()

   print(env.str('UNQUOTED_CERT', multiline=True))
   # ---BEGIN---
   # ---END---

   print(env.str('UNQUOTED_CERT', multiline=False))
   # ---BEGIN---\r\n---END---

   print(env.str('QUOTED_CERT', multiline=True))
   # ---BEGIN---
   # ---END---

   print(env.str('QUOTED_CERT', multiline=False))
   # ---BEGIN---\r\n---END---

   print(env.str('ESCAPED_CERT', multiline=True))
   # ---BEGIN---\
   # ---END---

   print(env.str('ESCAPED_CERT', multiline=False))
   # ---BEGIN---\\n---END---

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


Escape Proxy
============

If you're having trouble with values starting with dollar sign ($) without the intention of proxying the value to
another, You should enable the ``escape_proxy`` and prepend a backslash to it.

.. code-block:: python

    import environ

    env = environ.Env()
    env.escape_proxy = True

    # ESCAPED_VAR=\$baz
    env.str('ESCAPED_VAR')  # $baz


Reading env files
=================

.. _multiple-env-files-label:

Multiple env files
------------------

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
-----------------------------------

It is possible to use of :py:class:`pathlib.Path` objects when reading environment
file from the filesystem:

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


.. _overwriting-existing-env:

Overwriting existing environment values from env files
------------------------------------------------------

If you want variables set within your env files to take higher precedence than
an existing set environment variable, use the ``overwrite=True`` argument of
:meth:`.environ.Env.read_env`. For example:

.. code-block:: python

   env = environ.Env()
   env.read_env(BASE_DIR('.env'), overwrite=True)


Handling prefixes
=================

Sometimes it is desirable to be able to prefix all environment variables. For
example, if you are using Django, you may want to prefix all environment
variables with ``DJANGO_``. This can be done by setting the ``prefix``
to desired prefix. For example:

**.env file**:

.. code-block:: shell

   # .env file contents
   DJANGO_TEST="foo"

**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ


   env = environ.Env()
   env.prefix = 'DJANGO_'

   env.str('TEST')  # foo
