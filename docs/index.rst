Welcome to Django-environ's documentation!
==========================================

.. automodule:: environ.environ

.. include:: ../README.rst

environ.Env
===========

..  autoclass:: environ.environ.Env

    ..  autoattribute:: BOOLEAN_TRUE_STRINGS
    ..  autoattribute:: DB_SCHEMES
    ..  autoattribute:: DEFAULT_DATABASE_ENV
    ..  autoattribute:: CACHE_SCHEMES
    ..  autoattribute:: DEFAULT_CACHE_ENV
    ..  autoattribute:: EMAIL_SCHEMES
    ..  autoattribute:: DEFAULT_EMAIL_ENV
    ..  autoattribute:: SEARCH_SCHEMES
    ..  autoattribute:: DEFAULT_SEARCH_ENV

    ..  automethod:: __call__
    ..  automethod:: str
    ..  automethod:: bool
    ..  automethod:: int
    ..  automethod:: float
    ..  automethod:: json
    ..  automethod:: list
    ..  automethod:: dict
    ..  automethod:: url
    ..  automethod:: db_url
    ..  automethod:: cache_url
    ..  automethod:: email_url
    ..  automethod:: search_url
    ..  automethod:: path

    ..  automethod:: read_env
    ..  automethod:: db_url_config
    ..  automethod:: cache_url_config
    ..  automethod:: email_url_config
    ..  automethod:: search_url_config
    ..  automethod:: get_value
    ..  automethod:: parse_value


environ.Path
============

..  autoclass:: environ.environ.Path

    ..  py:attribute:: root -> Retrieve absolute path
    ..  automethod:: __call__
    ..  automethod:: path
    ..  automethod:: file


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

