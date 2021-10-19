# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

"""The top-level module for django-environ package.

This module tracks the version of the package as well as the base
package info used by various functions within django-environ.

Misc variables:

    __copyright__
    __version__
    __license__
    __author__
    __author_email__
    __maintainer__
    __maintainer_email__
    __url__
    __description__

Refer to the `documentation <https://django-environ.readthedocs.org/>`_
for details on the use of this package.
"""

from .environ import *


__copyright__ = 'Copyright (C) 2021 Daniele Faraglia'
__version__ = '0.8.1'
__license__ = 'MIT'
__author__ = 'Daniele Faraglia'
__author_email__ = 'daniele.faraglia@gmail.com'
__maintainer__ = 'Serghei Iakovlev'
__maintainer_email__ = 'egrep@protonmail.ch'
__url__ = 'https://django-environ.readthedocs.org'
__description__ = 'A package that allows you to utilize 12factor inspired environment variables to configure your Django application.'  # noqa: E501
