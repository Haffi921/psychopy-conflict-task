import pytest

from conflict_task.util.dictionary import (
    get_or_fatal_exit,
    get_type,
    get_type_or_fatal_exit,
)


@pytest.mark.parametrize("key", ["one_key", "another_key", "silly_duck"])
class TestGetOrFatalExit:
    def test_get_or_fatal_exit_null_values(
        self, key: str, capsys: pytest.CaptureFixture
    ):
        dictionary = {
            "one_key": [],
            "another_key": {},
            "silly_duck": 0,
        }
        msg = f"dictionary must have key: {key}"

        value = get_or_fatal_exit(dictionary, key, msg)
        error_output = capsys.readouterr().out

        assert dictionary[key] == value
        assert msg not in error_output and error_output == ""

    def test_get_or_fatal_exit(self, key: str, capsys: pytest.CaptureFixture):
        dictionary = {
            "one_key": ["a"],
            "another_key": {"a": 4},
            "silly_duck": 213,
        }
        msg = f"dictionary must have key: {key}"

        value = get_or_fatal_exit(dictionary, key, msg)
        error_output = capsys.readouterr().out

        assert dictionary[key] == value
        assert msg not in error_output and error_output == ""

    def test_get_or_fatal_exit_error(self, key: str, capsys: pytest.CaptureFixture):
        dictionary = {
            "different_key": ["a"],
            "these_are_not_the_droids_you_are_looking_for": 42,
        }
        msg = f"dictionary must have key: {key}"

        with pytest.raises(SystemExit):
            get_or_fatal_exit(dictionary, key, msg)

        assert msg in capsys.readouterr().out


@pytest.mark.parametrize(
    "key, type_name",
    [
        ("bool", bool),
        ("int", int),
        ("float", float),
        ("str", str),
        ("tuple", tuple),
        ("list", list),
        ("dict", dict),
    ],
)
class TestGetTypeOrFatalExit:
    def test_get_type_or_fatal_exit_null_values(
        self, key: str, type_name: object, capsys: pytest.CaptureFixture
    ):
        dictionary = {
            "bool": False,
            "int": 0,
            "float": 0.0,
            "str": "",
            "tuple": (),
            "list": [],
            "dict": {},
        }

        msg = f"dictionary must have key: {key}"
        error_msg = f"'{key}' must be of type '{type_name}'"

        value = get_type_or_fatal_exit(dictionary, key, type_name, msg)
        error_output = capsys.readouterr().out

        assert dictionary[key] == value
        assert error_msg not in error_output and error_output == ""

    def test_get_type_or_fatal_exit(
        self, key: str, type_name: object, capsys: pytest.CaptureFixture
    ):
        dictionary = {
            "bool": True,
            "int": 123,
            "float": 21.2323,
            "str": "Hello, World",
            "tuple": (32, "Silly duck"),
            "list": [124, 983, 2324],
            "dict": {"a": 32, "b": "None"},
        }

        msg = f"dictionary must have key: {key}"
        error_msg = f"'{key}' must be of type '{type_name}'"

        value = get_type_or_fatal_exit(dictionary, key, type_name, msg)
        error_output = capsys.readouterr().out

        assert dictionary[key] == value
        assert error_msg not in error_output and error_output == ""

    def test_get_type_or_fatal_exit_wrong_type(
        self, key: str, type_name: object, capsys: pytest.CaptureFixture
    ):
        dictionary = {
            "bool": "True",
            "int": 123.2,
            "float": 21,
            "str": ["Hello, World"],
            "tuple": {32: "Silly duck"},
            "list": (124, 983, 2324),
            "dict": ["a", 32, "b", "None"],
        }

        msg = f"dictionary must have key: {key}"
        error_msg = f"'{key}' must be of type '{type_name}'"

        with pytest.raises(SystemExit):
            get_type_or_fatal_exit(dictionary, key, type_name, msg)

        assert error_msg in capsys.readouterr().out

    def test_get_type_or_fatal_exit_nothing_to_get(
        self, key: str, type_name: object, capsys: pytest.CaptureFixture
    ):
        dictionary = {}

        msg = f"dictionary must have key: {key}"

        with pytest.raises(SystemExit):
            get_type_or_fatal_exit(dictionary, key, type_name, msg)

        assert msg in capsys.readouterr().out


@pytest.mark.parametrize(
    "key, type_name",
    [
        ("bool", bool),
        ("int", int),
        ("float", float),
        ("str", str),
        ("tuple", tuple),
        ("list", list),
        ("dict", dict),
    ],
)
class TestGetType:
    def test_get_type_null_values(
        self, key: str, type_name: object, capsys: pytest.CaptureFixture
    ):
        dictionary = {
            "bool": False,
            "int": 0,
            "float": 0.0,
            "str": "",
            "tuple": (),
            "list": [],
            "dict": {},
        }

        error_msg = f"'{key}' must be of type '{type_name}'"

        value = get_type(dictionary, key, type_name)
        error_output = capsys.readouterr().out

        assert dictionary[key] == value
        assert error_msg not in error_output and error_output == ""

    def test_get_type(self, key: str, type_name: object, capsys: pytest.CaptureFixture):
        dictionary = {
            "bool": True,
            "int": 123,
            "float": 21.2323,
            "str": "Hello, World",
            "tuple": (32, "Silly duck"),
            "list": [124, 983, 2324],
            "dict": {"a": 32, "b": "None"},
        }

        error_msg = f"'{key}' must be of type '{type_name}'"

        value = get_type(dictionary, key, type_name)
        error_output = capsys.readouterr().out

        assert dictionary[key] == value
        assert error_msg not in error_output and error_output == ""

    def test_get_type_wrong_type(
        self, key: str, type_name: object, capsys: pytest.CaptureFixture
    ):
        dictionary = {
            "bool": "True",
            "int": 123.2,
            "float": 21,
            "str": ["Hello, World"],
            "tuple": {32: "Silly duck"},
            "list": (124, 983, 2324),
            "dict": ["a", 32, "b", "None"],
        }

        error_msg = f"'{key}' must be of type '{type_name}'"

        with pytest.raises(SystemExit):
            get_type(dictionary, key, type_name)

        assert error_msg in capsys.readouterr().out

    def test_get_type_nothing_to_get(self, key: str, type_name: object):
        dictionary = {}

        value = get_type(dictionary, key, type_name)

        assert value is None

    def test_get_type_nothing_to_get_valid_backup(self, key: str, type_name: object):
        backup_dictionary = {
            "bool": True,
            "int": 123,
            "float": 21.2323,
            "str": "Hello, World",
            "tuple": (32, "Silly duck"),
            "list": [124, 983, 2324],
            "dict": {"a": 32, "b": "None"},
        }

        dictionary = {}

        value = get_type(dictionary, key, type_name, backup_dictionary[key])

        assert value == backup_dictionary[key]

    def test_get_type_nothing_to_get_wrong_backup(
        self, key: str, type_name: object, capsys: pytest.CaptureFixture
    ):
        backup_dictionary = {
            "bool": "True",
            "int": 123.2,
            "float": 21,
            "str": ["Hello, World"],
            "tuple": {32: "Silly duck"},
            "list": (124, 983, 2324),
            "dict": ["a", 32, "b", "None"],
        }

        dictionary = {}

        error_msg = f"'{key}' must be of type '{type_name}'"

        with pytest.raises(SystemExit):
            value = get_type(dictionary, key, type_name, backup_dictionary[key])

        assert error_msg in capsys.readouterr().out
