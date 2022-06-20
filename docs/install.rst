============
Installation
============


Requirements
============

* `Django <https://www.djangoproject.com/>`_ >= 1.11
* `Python <https://www.python.org/>`_ >= 3.5

Installing django-environ
=========================

django-environ is a Python-only package `hosted_on_pypi`_.
The recommended installation method is `pip`_-installing into a
:mod:`virtualenv <python:venv>`:

.. code-block:: console

   $ python -m pip install django-environ

.. note::

   After installing django-environ, no need to add it to ``INSTALLED_APPS``.


.. _hosted_on_pypi: https://pypi.org/project/django-environ/
.. _pip: https://pip.pypa.io/en/stable/


Unstable version
================

The master of all the material is the Git repository at https://github.com/joke2k/django-environ.
So, you can also install the latest unreleased development version directly from the
``develop`` branch on GitHub. It is a work-in-progress of a future stable release so the
experience might be not as smooth:

.. code-block:: console

   $ pip install -e git://github.com/joke2k/django-environ.git#egg=django-environ
   # OR
   $ pip install --upgrade https://github.com/joke2k/django-environ.git/archive/develop.tar.gz

This command will download the latest version of django-environ and install
it to your system.

.. note::

   The ``develop`` branch will always contain the latest unstable version, so the experience
   might be not as smooth. If you wish to check older versions or formal, tagged release,
   please switch to the relevant `tag <https://github.com/joke2k/django-environ/tags>`_.

More information about ``pip`` and PyPI can be found here:

* `Install pip <https://pip.pypa.io/en/latest/installing/>`_
* `Python Packaging User Guide <https://packaging.python.org/en/latest/>`_
