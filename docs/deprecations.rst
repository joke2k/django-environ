============
Deprecations
============

Features deprecated in 0.10.0
=============================

Python
------

* Support of Python < 3.6 is deprecated and will be removed
  in next major version.


Features deprecated in 0.9.0
============================

Methods
-------

* The ``environ.Env.unicode`` method is deprecated as it was used
  for Python 2.x only. Use :meth:`.environ.Env.str` instead.
