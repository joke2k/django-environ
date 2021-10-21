# This file is part of the django-environ.
#
# Copyright (c) 2021, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import pytest

from environ import Env


def test_solr_parsing(solr_url):
    url = Env.search_url_config(solr_url)

    assert len(url) == 2
    assert url['ENGINE'] == 'haystack.backends.solr_backend.SolrEngine'
    assert url['URL'] == 'http://127.0.0.1:8983/solr'


def test_solr_multicore_parsing(solr_url):
    timeout = 360
    index = 'solr_index'
    url = '{}/{}?TIMEOUT={}'.format(solr_url, index, timeout)
    url = Env.search_url_config(url)

    assert url['ENGINE'] == 'haystack.backends.solr_backend.SolrEngine'
    assert url['URL'] == 'http://127.0.0.1:8983/solr/solr_index'
    assert url['TIMEOUT'] == timeout
    assert 'INDEX_NAME' not in url
    assert 'PATH' not in url


@pytest.mark.parametrize(
    'url,engine',
    [
        ('elasticsearch://127.0.0.1:9200/index',
         'elasticsearch_backend.ElasticsearchSearchEngine'),
        ('elasticsearch2://127.0.0.1:9200/index',
         'elasticsearch2_backend.Elasticsearch2SearchEngine'),
        ('elasticsearch5://127.0.0.1:9200/index',
         'elasticsearch5_backend.Elasticsearch5SearchEngine'),
        ('elasticsearch7://127.0.0.1:9200/index',
         'elasticsearch7_backend.Elasticsearch7SearchEngine'),
    ],
    ids=[
        'elasticsearch',
        'elasticsearch2',
        'elasticsearch5',
        'elasticsearch7',
    ]
)
def test_elasticsearch_parsing(url, engine):
    """Ensure all supported Elasticsearch engines are recognized."""
    timeout = 360
    url = '{}?TIMEOUT={}'.format(url, timeout)
    url = Env.search_url_config(url)

    assert url['ENGINE'] == 'haystack.backends.{}'.format(engine)
    assert 'INDEX_NAME' in url.keys()
    assert url['INDEX_NAME'] == 'index'
    assert 'TIMEOUT' in url.keys()
    assert url['TIMEOUT'] == timeout
    assert 'PATH' not in url


@pytest.mark.parametrize('storage', ['file', 'ram'])
def test_whoosh_parsing(whoosh_url, storage):
    post_limit = 128 * 1024 * 1024
    url = '{}?STORAGE={}&POST_LIMIT={}'.format(whoosh_url, storage, post_limit)
    url = Env.search_url_config(url)

    assert url['ENGINE'] == 'haystack.backends.whoosh_backend.WhooshEngine'
    assert 'PATH' in url.keys()
    assert url['PATH'] == '/home/search/whoosh_index'
    assert 'STORAGE' in url.keys()
    assert url['STORAGE'] == storage
    assert 'POST_LIMIT' in url.keys()
    assert url['POST_LIMIT'] == post_limit
    assert 'INDEX_NAME' not in url


@pytest.mark.parametrize('flags', ['myflags'])
def test_xapian_parsing(xapian_url, flags):
    url = '{}?FLAGS={}'.format(xapian_url, flags)
    url = Env.search_url_config(url)

    assert url['ENGINE'] == 'haystack.backends.xapian_backend.XapianEngine'
    assert 'PATH' in url.keys()
    assert url['PATH'] == '/home/search/xapian_index'
    assert 'FLAGS' in url.keys()
    assert url['FLAGS'] == flags
    assert 'INDEX_NAME' not in url


def test_simple_parsing(simple_url):
    url = Env.search_url_config(simple_url)

    assert url['ENGINE'] == 'haystack.backends.simple_backend.SimpleEngine'
    assert 'INDEX_NAME' not in url
    assert 'PATH' not in url


def test_common_args_parsing(search_url):
    excluded_indexes = 'myapp.indexes.A,myapp.indexes.B'
    include_spelling = 1
    batch_size = 100
    params = 'EXCLUDED_INDEXES={}&INCLUDE_SPELLING={}&BATCH_SIZE={}'.format(
        excluded_indexes,
        include_spelling,
        batch_size
    )

    url = '?'.join([search_url, params])
    url = Env.search_url_config(url)

    assert 'EXCLUDED_INDEXES' in url.keys()
    assert 'myapp.indexes.A' in url['EXCLUDED_INDEXES']
    assert 'myapp.indexes.B' in url['EXCLUDED_INDEXES']
    assert 'INCLUDE_SPELLING' in url.keys()
    assert url['INCLUDE_SPELLING']
    assert 'BATCH_SIZE' in url.keys()
    assert url['BATCH_SIZE'] == 100
