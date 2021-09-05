# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import os
import pathlib
import sys

import pytest


@pytest.fixture
def solr_url():
    """Return Solr URL."""
    return 'solr://127.0.0.1:8983/solr'


@pytest.fixture
def whoosh_url():
    """Return Whoosh URL."""
    return 'whoosh:///home/search/whoosh_index'


@pytest.fixture
def xapian_url():
    """Return Xapian URL."""
    return 'xapian:///home/search/xapian_index'


@pytest.fixture
def simple_url():
    """Return simple URL."""
    return 'simple:///'


@pytest.fixture
def volume():
    """Return volume name is OS is Windows, otherwise None."""
    if sys.platform == 'win32':
        return pathlib.Path(os.getcwd()).parts[0]
    return None


@pytest.fixture(params=[
    'solr://127.0.0.1:8983/solr',
    'elasticsearch://127.0.0.1:9200/index',
    'whoosh:///home/search/whoosh_index',
    'xapian:///home/search/xapian_index',
    'simple:///'
])
def search_url(request):
    """Return Search Engine URL."""
    return request.param
