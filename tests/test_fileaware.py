# This file is part of the django-environ.
#
# Copyright (c) 2024-present, Daniele Faraglia <daniele.faraglia@gmail.com>
# Copyright (c) 2021-2024, Serghei Iakovlev <oss@serghei.pl>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

import os
import tempfile
from contextlib import contextmanager

import pytest

import environ


@contextmanager
def make_temp_file(text):
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(text)
        f.close()
    try:
        yield f.name
    finally:
        if os.path.exists(f.name):
            os.unlink(f.name)


@pytest.fixture
def tmp_f():
    with make_temp_file(text="fish") as f_name:
        yield f_name


@pytest.fixture(params=[2, 3])
def nested_file_values(tmp_path, request):
    value = tmp_path / 'value'
    value.write_text('fish', encoding='utf-8')
    values = {'ANIMAL': 'cat', 'ANIMAL_FILE': str(value)}
    for depth in range(2, request.param + 1):
        pointer = tmp_path / f'pointer-{depth}'
        pointer.write_text(
            values['ANIMAL' + '_FILE' * (depth - 1)], encoding='utf-8'
        )
        values['ANIMAL' + '_FILE' * depth] = str(pointer)
    return values


def test_mapping(tmp_f):
    env = environ.FileAwareMapping(env={"ANIMAL_FILE": tmp_f})
    assert env["ANIMAL"] == "fish"


def test_precidence(tmp_f):
    env = environ.FileAwareMapping(
        env={
            "ANIMAL_FILE": tmp_f,
            "ANIMAL": "cat",
        }
    )
    assert env["ANIMAL"] == "fish"


def test_missing_file_raises_exception():
    env = environ.FileAwareMapping(env={"ANIMAL_FILE": "non-existant-file"})
    with pytest.raises(FileNotFoundError):
        env["ANIMAL"]


def test_iter():
    env = environ.FileAwareMapping(
        env={
            "ANIMAL_FILE": "some-file",
            "VEGETABLE": "leek",
            "VEGETABLE_FILE": "some-vegetable-file",
        }
    )
    keys = set(env)
    assert keys == {"ANIMAL_FILE", "ANIMAL", "VEGETABLE", "VEGETABLE_FILE"}
    assert "ANIMAL" in keys


def test_len():
    env = environ.FileAwareMapping(
        env={
            "ANIMAL_FILE": "some-file",
            "VEGETABLE": "leek",
            "VEGETABLE_FILE": "some-vegetable-file",
        }
    )
    assert len(env) == 4


def test_cache(tmp_f):
    env = environ.FileAwareMapping(env={"ANIMAL_FILE": tmp_f})
    assert env["ANIMAL"] == "fish"

    with open(tmp_f, "w") as f:
        f.write("cat")
    assert env["ANIMAL"] == "fish"

    os.unlink(tmp_f)
    assert not os.path.exists(env["ANIMAL_FILE"])
    assert env["ANIMAL"] == "fish"


def test_no_cache(tmp_f):
    env = environ.FileAwareMapping(
        cache=False,
        env={"ANIMAL_FILE": tmp_f},
    )
    assert env["ANIMAL"] == "fish"

    with open(tmp_f, "w") as f:
        f.write("cat")
    assert env["ANIMAL"] == "cat"

    os.unlink(tmp_f)
    assert not os.path.exists(env["ANIMAL_FILE"])
    with pytest.raises(FileNotFoundError):
        assert env["ANIMAL"]


def test_setdefault(tmp_f):
    env = environ.FileAwareMapping(env={"ANIMAL_FILE": tmp_f})
    assert env.setdefault("FRUIT", "apple") == "apple"
    assert env.setdefault("ANIMAL", "cat") == "fish"
    assert env.env == {"ANIMAL_FILE": tmp_f, "FRUIT": "apple"}


class TestDelItem:
    def test_del_key(self):
        env = environ.FileAwareMapping(env={"FRUIT": "apple"})
        del env["FRUIT"]
        with pytest.raises(KeyError):
            env["FRUIT"]

    def test_del_key_with_file_key(self):
        env = environ.FileAwareMapping(env={"ANIMAL_FILE": "some-file"})
        del env["ANIMAL"]
        with pytest.raises(KeyError):
            env["ANIMAL"]

    def test_del_shadowed_key_with_file_key(self):
        env = environ.FileAwareMapping(
            env={"ANIMAL_FILE": "some-file", "ANIMAL": "cat"}
        )
        del env["ANIMAL"]
        with pytest.raises(KeyError):
            env["ANIMAL"]

    def test_del_file_key(self):
        env = environ.FileAwareMapping(
            env={
                "ANIMAL_FILE": "some-file",
                "ANIMAL": "fish",
            }
        )
        del env["ANIMAL_FILE"]
        assert env["ANIMAL"] == "fish"

    def test_del_file_key_clears_cache(self, tmp_f):
        env = environ.FileAwareMapping(
            env={
                "ANIMAL_FILE": tmp_f,
                "ANIMAL": "cat",
            }
        )
        assert env["ANIMAL"] == "fish"
        del env["ANIMAL_FILE"]
        assert env["ANIMAL"] == "cat"

    @pytest.mark.parametrize('cache', [True, False])
    def test_del_nested_logical_key(self, nested_file_values, cache):
        env = environ.FileAwareMapping(nested_file_values, cache=cache)
        assert env['ANIMAL'] == 'fish'
        del env['ANIMAL']
        assert list(env) == []
        assert len(env) == 0
        assert 'ANIMAL' not in env
        with pytest.raises(KeyError):
            env['ANIMAL']

    @pytest.mark.parametrize('cache', [True, False])
    def test_del_nested_file_key_restores_fallback(self, nested_file_values, cache):
        env = environ.FileAwareMapping(nested_file_values, cache=cache)
        assert env['ANIMAL'] == 'fish'
        del env['ANIMAL_FILE']
        assert env['ANIMAL'] == 'cat'
        assert list(env) == ['ANIMAL']

    @pytest.mark.parametrize('cache', [True, False])
    def test_clear_nested_mapping_restores_default(
        self, nested_file_values, cache, monkeypatch
    ):
        env = environ.FileAwareMapping(nested_file_values, cache=cache)
        monkeypatch.setattr(environ.FileAwareEnv, 'ENVIRON', env)
        config = environ.FileAwareEnv()
        env.clear()
        assert list(env) == []
        assert len(env) == 0
        assert config('ANIMAL', default='default') == 'default'


class TestSetItem:
    def test_set_key(self):
        env = environ.FileAwareMapping(env={"FRUIT": "apple"})
        env["FRUIT"] = "banana"
        assert env["FRUIT"] == "banana"

    def test_cant_override_key_with_file_key(self, tmp_f):
        env = environ.FileAwareMapping(
            env={
                "FRUIT": "apple",
                "FRUIT_FILE": tmp_f,
            }
        )
        with open(tmp_f, "w") as f:
            f.write("banana")
        env["FRUIT"] = "cucumber"
        assert env["FRUIT"] == "banana"

    def test_set_file_key(self, tmp_f):
        env = environ.FileAwareMapping(env={"ANIMAL": "cat"})
        env["ANIMAL_FILE"] = tmp_f
        assert env["ANIMAL"] == "fish"

    def test_change_file_key_clears_cache(self, tmp_f):
        env = environ.FileAwareMapping(env={"ANIMAL_FILE": tmp_f})
        assert env["ANIMAL"] == "fish"
        with make_temp_file(text="cat") as new_tmp_f:
            env["ANIMAL_FILE"] = new_tmp_f
            assert env["ANIMAL"] == "cat"
