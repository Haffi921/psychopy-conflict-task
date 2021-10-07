import pytest

from conflict_task.component import CorrectResponseComponent, ResponseComponent


def test_response_has_no_keys(capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        ResponseComponent({})

    assert "Response component - Must have a 'keys' setting" in capsys.readouterr().out


def test_response_has_non_list_keys(capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        ResponseComponent({"keys": {}})

    assert f"'keys' must be of type '{list}'" in capsys.readouterr().out


def test_response_has_keys_of_no_length(capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        ResponseComponent({"keys": []})

    assert (
        "Response component - Setting 'keys' must include some keys"
        in capsys.readouterr().out
    )


def test_response_has_non_str_keys(capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        ResponseComponent({"keys": ["a", "d", 234]})

    assert (
        "Response component - Keys specified in 'keys' must be strings"
        in capsys.readouterr().out
    )


def test_response_has_valid_keys():
    keys = ["a", "b", "c", "d"]
    response = ResponseComponent({"keys": keys})

    assert response.keys == keys


def test_correct_response_no_correct_key(capsys: pytest.CaptureFixture):
    keys = ["a", "b", "c", "d"]
    with pytest.raises(SystemExit):
        CorrectResponseComponent({"keys": keys, "variable": {}})

    assert (
        "CorrectResponse component - 'correct_key' must be a key in variable factors"
        in capsys.readouterr().out
    )


def test_correct_answer_valid_correct_key():
    keys = ["a", "b", "c", "d"]
    response = CorrectResponseComponent(
        {"keys": keys, "variable": {"correct_key": "correct"}}
    )

    assert response.variable_factor["correct_key"] == "correct"
