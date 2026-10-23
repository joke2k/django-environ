# This file is part of the django-environ.
#
# Copyright (c) 2024-present, Daniele Faraglia <daniele.faraglia@gmail.com>
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

from django.core.exceptions import ImproperlyConfigured
import pytest

from environ import Env


def test_smtp_parsing():
    url = 'smtps://user@domain.com:password@smtp.example.com:587'
    url = Env.email_url_config(url)

    assert len(url) == 7

    assert url['EMAIL_BACKEND'] == 'django.core.mail.backends.smtp.EmailBackend'
    assert url['EMAIL_HOST'] == 'smtp.example.com'
    assert url['EMAIL_HOST_PASSWORD'] == 'password'
    assert url['EMAIL_HOST_USER'] == 'user@domain.com'
    assert url['EMAIL_PORT'] == 587
    assert url['EMAIL_USE_TLS'] is True
    assert url['EMAIL_FILE_PATH'] == ''


def test_custom_email_backend():
    """Override EMAIL_BACKEND determined from schema."""
    url = 'smtps://user@domain.com:password@smtp.example.com:587'

    backend = 'mypackage.backends.whatever'
    url = Env.email_url_config(url, backend=backend)

    assert url['EMAIL_BACKEND'] == backend


def test_mailer_parsing():
    url = 'smtps://user@domain.com:password@smtp.example.com:587'

    assert Env.mailer_url_config(url) == {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': 'smtp.example.com',
            'password': 'password',
            'port': 587,
            'use_tls': True,
            'username': 'user@domain.com',
        },
    }


def test_mailer_extra_options_override_url_options_without_casting():
    url = 'smtp+ssl://smtp.example.com?timeout=30'
    extra_options = {
        'timeout': 45,
        'use_ssl': False,
        'custom': {'retries': 3},
    }

    config = Env.mailer_url_config(url, extra_options=extra_options)

    assert config['OPTIONS'] == {
        'host': 'smtp.example.com',
        'timeout': 45,
        'use_ssl': False,
        'custom': {'retries': 3},
    }


def test_mailer_file_parsing():
    url = 'filemail:///tmp/email'

    assert Env.mailer_url_config(url) == {
        'BACKEND': 'django.core.mail.backends.filebased.EmailBackend',
        'OPTIONS': {'file_path': 'tmp/email'},
    }


def test_mailer_options_parsing_with_pre_6_1_format():
    url = 'smtp+ssl://smtp.example.com?EMAIL_USE_SSL=false&timeout=30'

    assert Env.mailer_url_config(url) == {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': 'smtp.example.com',
            'timeout': 30,
            'use_ssl': 'false',
        },
    }

def test_mailer_options_parsing_with_6_1_format():
    url = 'smtp+ssl://smtp.example.com?use_ssl=false&timeout=30'

    assert Env.mailer_url_config(url) == {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': 'smtp.example.com',
            'timeout': 30,
            'use_ssl': 'false',
        },
    }



def test_mailer_custom_backend():
    backend = 'mypackage.backends.whatever'

    assert Env.mailer_url_config(
        'smtp://smtp.example.com', backend=backend
    )['BACKEND'] == backend


def test_invalid_mailer_schema():
    with pytest.raises(ImproperlyConfigured) as exc:
        Env.mailer_url_config('smtp3://smtp.example.com')
    assert 'Invalid email schema smtp3' == str(exc.value)


def test_smtp_ssl_and_options_parsing():
    url = (
        "smtp+ssl://user@domain.com:password@smtp.example.com:465"
        "?EMAIL_USE_SSL=true&timeout=30"
    )
    url = Env.email_url_config(url)

    assert url['EMAIL_BACKEND'] == 'django.core.mail.backends.smtp.EmailBackend'
    assert url['EMAIL_USE_SSL'] == 'true'
    assert url['OPTIONS'] == {'TIMEOUT': 30}


def test_invalid_email_schema():
    with pytest.raises(ImproperlyConfigured) as exc:
        Env.email_url_config('smtp3://user:password@example.com:25')
    assert 'Invalid email schema smtp3' == str(exc.value)
