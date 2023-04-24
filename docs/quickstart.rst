===========
Quick Start
===========

Usage
=====

Create a ``.env`` file in project root directory. The file format can be understood
from the example below:

.. code-block:: shell

   DEBUG=on
   SECRET_KEY=your-secret-key
   DATABASE_URL=psql://user:un-githubbedpassword@127.0.0.1:8458/database
   SQLITE_URL=sqlite:///my-local-sqlite.db
   CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
   REDIS_URL=rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password=ungithubbed-secret

And use it with ``settings.py`` as follows:

.. include:: ../README.rst
   :start-after: -code-begin-
   :end-before: -overview-

Variables can contain references to another variables: ``$VAR`` or ``${VAR}``.
Referenced variables are searched in the environment and within all definitions
in the ``.env`` file. References are checked for recursion (self-reference).
Exception is thrown if any reference results in infinite loop on any level
of recursion. Variable values are substituted similar to shell parameter
expansion. Example:

.. code-block:: shell

   # shell
   export POSTGRES_USERNAME='user' POSTGRES_PASSWORD='SECRET'

.. code-block:: shell

   # .env
   POSTGRES_HOSTNAME='example.com'
   POSTGRES_DB='database'
   DATABASE_URL="postgres://${POSTGRES_USERNAME}:${POSTGRES_PASSWORD}@${POSTGRES_HOSTNAME}:5432/${POSTGRES_DB}"

The value of ``DATABASE_URL`` variable will become
``postgres://user:SECRET@example.com:5432/database``.

The ``.env`` file should be specific to the environment and not checked into
version control, it is best practice documenting the ``.env`` file with an example.
For example, you can also add ``.env.dist`` with a template of your variables to
the project repo. This file should describe the mandatory variables for the
Django application, and it can be committed to version control.  This provides a
useful reference and speeds up the on-boarding process for new team members, since
the time to dig through the codebase to find out what has to be set up is reduced.

A good ``.env.dist`` could look like this:

.. code-block:: shell

   # SECURITY WARNING: don't run with the debug turned on in production!
   DEBUG=True

   # Should robots.txt allow everything to be crawled?
   ALLOW_ROBOTS=False

   # SECURITY WARNING: keep the secret key used in production secret!
   SECRET_KEY=secret

   # A list of all the people who get code error notifications.
   ADMINS="John Doe <john@example.com>, Mary <mary@example.com>"

   # A list of all the people who should get broken link notifications.
   MANAGERS="Blake <blake@cyb.org>, Alice Judge <alice@cyb.org>"

   # By default, Django will send system email from root@localhost.
   # However, some mail providers reject all email from this address.
   SERVER_EMAIL=webmaster@example.com
