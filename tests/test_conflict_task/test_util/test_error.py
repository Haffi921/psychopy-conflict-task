import pytest

from conflict_task.util import fatal_exit, true_or_fatal_exit


@pytest.mark.parametrize("msg", ["One error", "Another error", "Silly ducks"])
def test_fatal_exit(msg: str, capsys: pytest.CaptureFixture):
    def call_fatal(msg, test=True):
        if test:
            fatal_exit(msg)

    with pytest.raises(SystemExit):
        call_fatal(msg)

    assert msg in capsys.readouterr().out


@pytest.mark.parametrize("msg", ["One error", "Another error", "Silly ducks"])
def test_true_or_fatal_exit_with_false(msg: str, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        true_or_fatal_exit(False, msg)

    assert msg in capsys.readouterr().out


@pytest.mark.parametrize("msg", ["One error", "Another error", "Silly ducks"])
def test_true_or_fatal_exit_with_true(msg: str, capsys: pytest.CaptureFixture):
    true_or_fatal_exit(True, msg)

    error_output = capsys.readouterr().out

    assert msg not in error_output and error_output == ""
