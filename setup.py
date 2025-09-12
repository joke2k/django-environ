#!/usr/bin/env python3
"""
Deprecated setup.py for django-environ.

This file is deprecated and will be removed in a future release.
Please use `python -m build` instead of `python setup.py` commands.

For more information, see:
https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
"""

import warnings

from setuptools import setup

# Issue deprecation warning
warnings.warn(
    "setup.py install is deprecated. "
    "Use `python -m pip install .` instead. "
    "Direct setup.py usage will be removed by 2025-Oct-31. See https://setuptools.pypa.io/en/stable/history.html#v80-1-0"
    "See https://packaging.python.org/en/latest/discussions/setup-py-deprecated/",
    DeprecationWarning,
    stacklevel=2
)


if __name__ == '__main__':
    # All configuration is now in pyproject.toml
    # This is just for backward compatibility
    setup()
