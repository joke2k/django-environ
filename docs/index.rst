Welcome to Django-environ's documentation!
==========================================

..  automodule:: environ.environ

This is your `settings.py` file before you have installed **django-environ**::

    import os
    SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'database',
            'USER': 'user',
            'PASSWORD': 'githubbedpassword',
            'HOST': '123.123.123.123',
            'PORT': '8458',
        }
        'extra': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'database.sqlite')
        }
    }

    MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')
    MEDIA_URL = 'media/'
    STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
    STATIC_URL = 'static/'

    SECRET_KEY = '...im incredibly still here...'

After::

    import environ
    root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
    env = environ.Env(DEBUG=(False,bool),) # set default values and casting

    SITE_ROOT = root()

    DEBUG = env('DEBUG') # False if not in os.environ
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
        'extra': env.db('SQLITE_DB_URL', default=root('database.sqlite'))
    }

    MEDIA_ROOT = root('assets')
    MEDIA_URL = 'media/'
    STATIC_ROOT = root('static')
    STATIC_URL = 'static/'

    SECRET_KEY = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ


DevMode
-------

Put your environment variables definition in a `.env` file::

    $ cat >.env <<EOM
    DEBUG=on
    SECRET_KEY=1110110010111101111011101111
    DATABASE_URL=postgres://uf07k1:wegauwhg@compute-1.amazonaws.com:5431/d8r827
    SQLITE_URL=sqlite:////var/db/myapp.db
    EOM

Then in your `settings.py` or `settings/dev.py`::

    import environ
    root = environ.Path(__file__) - 3
    env = environ.Env()

    env.read_env(root('.env'))

    ...

Tests
-----

::

    $ git clone git@github.com:joke2k/django-environ.git
    $ cd django-environ/
    $ python setup.py test


environ.Env
-----------

..  autoclass:: environ.environ.Env

    ..  autoattribute:: BOOLEAN_TRUE_STRINGS
    ..  autoattribute:: DB_SCHEMES
    ..  autoattribute:: DATABASE_URL

    ..  automethod:: __call__
    ..  automethod:: str
    ..  automethod:: bool
    ..  automethod:: int
    ..  automethod:: float
    ..  automethod:: json
    ..  automethod:: list
    ..  automethod:: dict
    ..  automethod:: url
    ..  automethod:: db
    ..  automethod:: path

    ..  automethod:: read_env
    ..  automethod:: db_url_config
    ..  automethod:: get_value
    ..  automethod:: parse_value


environ.Path
------------

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

