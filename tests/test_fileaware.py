# This file is part of the django-environ.
#
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
