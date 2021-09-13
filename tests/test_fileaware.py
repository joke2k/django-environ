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
