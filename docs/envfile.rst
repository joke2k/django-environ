====================
``.env`` file syntax
====================

``django-environ`` reads ``.env`` files with its own line-based parser. It is
neither a shell nor Docker Compose, and a file that works in one of those will
not always mean the same thing here. This page states exactly what
:meth:`.environ.Env.read_env` accepts.

Lines
=====

Each line is matched against a single pattern::

    [export ]KEY=VALUE

* **Blank lines** and lines whose first character is ``#`` are ignored.
* **Anything else that does not match** is skipped with an ``Invalid line``
  warning on the ``environ`` logger. It is not an error, so a malformed line
  fails silently unless logging is configured.
* A leading ``export`` is allowed, so the same file can be sourced by a shell.
  It must be exactly one space before the key.

Keys
====

A key may contain only ASCII letters, digits and underscores
(``[A-Za-z_0-9]``). Case is preserved, so ``debug`` and ``DEBUG`` are
different variables.

There must be **no whitespace around** ``=``. A line indented with leading
whitespace does not match either:

.. code-block:: shell

    # Parsed
    DEBUG=on
    export DEBUG=on

    # NOT parsed -- each of these is an "Invalid line"
    DEBUG = on
    MY-KEY=on
      DEBUG=on

Values
======

Everything after the first ``=`` is the value, so a value may itself contain
``=``. Values are always strings; the casting described in :doc:`types`
happens later, when you call ``env.bool()``, ``env.int()`` and so on.

**Whitespace is not stripped** from an unquoted value: trailing spaces after
the last visible character are part of it. Quote the value if you do not want
them.

Quoting
-------

A value wrapped in matching single or double quotes has those outer quotes
removed. Quotes anywhere else are kept as ordinary characters:

.. code-block:: shell

    A='hello world'      # -> hello world
    B="hello world"       # -> hello world
    C=it's                # -> it's
    D=say "what"          # -> say "what"

Inside **double** quotes a backslash escapes the next character, with one
deliberate exception: ``\n``, ``\r`` and ``\t`` are left alone so that the
two-character sequence survives into the value for code that wants to
interpret it later.

.. code-block:: shell

    E="a\"b"              # -> a"b
    F="a\zb"              # -> azb
    G="a\nb"              # -> a\nb   (backslash and n, not a newline)

Single quotes do no escape processing at all.

.. note::

   A value cannot span more than one line. There is no multi-line or heredoc
   syntax; a quote left open simply ends at the end of the line.

Comments
--------

By default a ``#`` inside a value is part of the value:

.. code-block:: shell

    KEY=abc#def           # -> abc#def

Passing ``parse_comments=True`` to :meth:`.environ.Env.read_env` strips from
the first ``#`` onwards. Be aware that for an unquoted value the whitespace
before the ``#`` is kept:

.. code-block:: shell

    # with parse_comments=True
    KEY=abc#def           # -> abc
    KEY=abc  # comment    # -> "abc  "  (note the trailing spaces)
    KEY='abc'  # comment  # -> abc

See :doc:`tips` for more on this option.

Differences from other ``.env`` formats
=======================================

Expecting one ``.env`` file to mean the same thing to ``django-environ``, a
shell and Docker Compose is asking for trouble. The differences that bite
most often:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Behaviour
     - ``django-environ``
     - Docker Compose / shell
   * - Wrapping quotes
     - Stripped
     - Docker Compose keeps them as part of the value
   * - Variable interpolation (``${OTHER}``)
     - Not performed; the literal text is kept
     - Both expand it
   * - Multi-line values
     - Not supported
     - Supported by both
   * - Whitespace around ``=``
     - Line is skipped
     - A shell rejects it; Docker Compose tolerates it

The classic failure is a quoted JSON value:

.. code-block:: shell

    DATABASES='{"default": {"ENGINE": "django.db.backends.sqlite3"}}'

``django-environ`` reads this as valid JSON. If Docker Compose has already
loaded the same file into the environment, the wrapping ``'`` characters are
still there and the value no longer parses.

If a single file has to serve both, avoid wrapping quotes entirely and avoid
values that need them.

.. warning::

   Environment variables that already exist take precedence over the file and
   are **not** overwritten, so a value Docker put in the environment wins over
   the one in the file. Pass ``overwrite=True`` to
   :meth:`.environ.Env.read_env` to reverse that.
