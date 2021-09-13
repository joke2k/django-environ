import os
import tempfile

import environ
import pytest


def test_mapping():
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write("fish")
        f.flush()

        env = environ.FileAwareMapping(env={"ANIMAL_FILE": f.name})
        assert env["ANIMAL"] == "fish"


def test_precidence():
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write("fish")
        f.flush()

        env = environ.FileAwareMapping(
            env={
                "ANIMAL_FILE": f.name,
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


def test_cache():
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write("fish")
        f.flush()

        env = environ.FileAwareMapping(env={"ANIMAL_FILE": f.name})
        assert env["ANIMAL"] == "fish"

        f.seek(0)
        f.write("cat")
        f.truncate()
        f.flush()
        assert env["ANIMAL"] == "fish"
    assert not os.path.exists(env["ANIMAL_FILE"])
    assert env["ANIMAL"] == "fish"


def test_no_cache():
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write("fish")
        f.flush()

        env = environ.FileAwareMapping(
            cache=False,
            env={"ANIMAL_FILE": f.name},
        )
        assert env["ANIMAL"] == "fish"

        f.seek(0)
        f.write("cat")
        f.truncate()
        f.flush()
        assert env["ANIMAL"] == "cat"

    assert not os.path.exists(env["ANIMAL_FILE"])
    with pytest.raises(FileNotFoundError):
        assert env["ANIMAL"]


def test_setdefault():
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write("fish")
        f.flush()
        env = environ.FileAwareMapping(env={"ANIMAL_FILE": f.name})
        assert env.setdefault("FRUIT", "apple") == "apple"
        assert env.setdefault("ANIMAL", "cat") == "fish"
        assert env.env == {"ANIMAL_FILE": f.name, "FRUIT": "apple"}


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

    def test_del_file_key(self):
        env = environ.FileAwareMapping(
            env={
                "ANIMAL_FILE": "some-file",
                "ANIMAL": "fish",
            }
        )
        del env["ANIMAL_FILE"]
        assert env["ANIMAL"] == "fish"


class TestSetItem:
    def test_set_key(self):
        env = environ.FileAwareMapping(env={"FRUIT": "apple"})
        env["FRUIT"] = "banana"
        assert env["FRUIT"] == "banana"

    def test_cant_override_key_with_file_key(self):
        with tempfile.NamedTemporaryFile(mode="w") as f:
            env = environ.FileAwareMapping(
                env={
                    "FRUIT": "apple",
                    "FRUIT_FILE": f.name,
                }
            )
            f.write("banana")
            f.flush()
            env["FRUIT"] = "cucumber"
            assert env["FRUIT"] == "banana"

    def test_set_file_key(self):
        env = environ.FileAwareMapping(env={"FRUIT": "apple"})
        with tempfile.NamedTemporaryFile(mode="w") as f:
            f.write("banana")
            f.flush()
            env["FRUIT_FILE"] = f.name
            assert env["FRUIT"] == "banana"
