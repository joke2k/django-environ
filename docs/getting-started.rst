===============
Getting Started
===============

Installation
============


Requirements
------------

* `Django <https://www.djangoproject.com/>`_ >= 1.11
* `Python <https://www.python.org/>`_ >= 3.4

Installing django-environ
_________________________

``django-environ`` is a Python-only package `hosted on PyPI <https://pypi.org/project/django-environ/>`_.
The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a virtualenv:

.. code-block:: shell

   $ python -m pip install django-environ

.. note::

   After installing ``django-environ``, no need to add it to ``INSTALLED_APPS``.

Unstable version
________________

The master of all the material is the Git repository at https://github.com/joke2k/django-environ.
So, you can also install the latest unreleased development version directly from the
``develop`` branch on GitHub. It is a work-in-progress of a future stable release so the
experience might be not as smooth.:

.. code-block:: shell

   $ pip install -e git://github.com/joke2k/django-environ.git#egg=django-environ
   # OR
   $ pip install --upgrade https://github.com/joke2k/django-environ.git/archive/develop.tar.gz

This command will download the latest version of ``django-environ`` and install
it to your system.

.. note::

   The ``develop`` branch will always contain the latest unstable version, so the experience
   might be not as smooth. If you wish to check older versions or formal, tagged release,
   please switch to the relevant `tag <https://github.com/joke2k/django-environ/tags>`_.

More information about ``pip`` and PyPI can be found here:

* `Install pip <https://pip.pypa.io/en/latest/installing/>`_
* `Python Packaging User Guide <https://packaging.python.org/>`_

Usage
-----

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

.. warning::

   Don't forget to add ``.env`` in your ``.gitignore``. You can also add
   ``.env.dist`` with a template of your variables to the project repo.

FAQ
---

- **Q:** What(where) is the root part of the project, is it part of the project where are settings?
- **A:** Where your ``manage.py`` file is (that is your project root directory).

- **Q:** What kind of file should ``.env`` be?
- **A:** ``.env`` is a plaint text file.

- **Q:** Should name of the file be simply ``.env`` (or ``something.env``)?
- **A:** Just ``.env``

- **Q:** Is ``.env`` file going to be imported in settings file?
- **A:** No need to import, ``django-environ`` automatically picks variables from there.
