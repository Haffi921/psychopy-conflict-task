import pytest

from conflict_task.component.response_component import (
    CorrectResponseComponent,
    ResponseComponent,
)
from conflict_task.component.visual_component import VisualComponent
from conflict_task.constants import INFINITY
from conflict_task.devices import input_device
from conflict_task.sequence._base_sequence import BaseSequence
from conflict_task.sequence.sequence import Sequence


def test_base_sequence_cannot_be_created(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        BaseSequence(win, input, {})

    assert (
        "An instance of BaseSequence should not be created nor run"
        in capsys.readouterr().out
    )


def test_empty_sequence(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(win, input, {})

    assert "UNKNOWN_SEQUENCE: Sequence has no components" in capsys.readouterr().out


def test_all_sequence_settings_are_set(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "wait_for_response": True,
            "cut_on_response": True,
            "timed": True,
            "timer": 18.0,
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
            ],
            "response": {"keys": ["space"]},
        },
    )

    assert sequence.name == "TestSequence"
    assert sequence.wait_for_response
    assert sequence.cut_on_response
    assert sequence.timed
    assert sequence.timer == 18.0


def test_empty_sequence_settings_are_set(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
            ]
        },
    )

    assert sequence.name == "UNKNOWN_SEQUENCE"
    assert not sequence.wait_for_response
    assert not sequence.cut_on_response
    assert not sequence.timed
    assert sequence.timer is None


def test_extra_sequence_settings_are_not_set(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "SillyDucks": 42,
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
            ],
        },
    )

    assert not hasattr(sequence, "SillyDucks")


def test_if_timer_is_not_set(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "NoTimerSequence",
                "timed": True,
                "visual_components": [{"name": "Text", "type": "TextStim", "spec": {}}],
            },
        )

    assert (
        "NoTimerSequence: If sequence is timed, please provide a timer"
        in capsys.readouterr().out
    )


def test_if_timer_is_negative(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "NegativeTimerSequence",
                "timed": True,
                "timer": -128.0,
                "visual_components": [{"name": "Text", "type": "TextStim", "spec": {}}],
            },
        )

    assert (
        "NegativeTimerSequence: Timer has to be greater than 0.0"
        in capsys.readouterr().out
    )


def test_if_timer_is_not_float(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "TextTimerSequence",
                "timed": True,
                "timer": "Hello",
                "visual_components": [{"name": "Text", "type": "TextStim", "spec": {}}],
            },
        )

    assert f"'timer' must be of type '{float}'" in capsys.readouterr().out


def test_empty_component_list_are_not_created(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "name": "SequenceWithEmptyComponentLists",
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
            ],
            "audio_components": [],
        },
    )

    assert len(sequence._get_all_components()) == 1


def test_empty_component_settings_give_error(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "SequenceWithEmptyComponentSettings",
                "visual_components": [{}, {}],
            },
        )

    assert capsys.readouterr().out != ""


def test_component_list_are_not_lists(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "SequenceWithNonListComponentLists",
                "visual_components": {23, 23242, 15},
            },
        )

    assert f"'visual_components' must be of type '{list}'" in capsys.readouterr().out


def test_component_settings_not_dicts(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "SequenceWithNonDictComponentSettings",
                "visual_components": [23, 23242, 15],
            },
        )

    assert (
        f"SequenceWithNonDictComponentSettings: Components settings need to be a dictionary"
        in capsys.readouterr().out
    )


def test_component_settings_work(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "spec": {},
                    "start": 5.0,
                    "stop": 7.0,
                }
            ],
        },
    )

    component = sequence._get_all_components()[0]

    assert component.name == "Text"
    assert type(component) == VisualComponent
    assert component.start_time == 5.0
    assert component.stop_time == 7.0


def test_correct_response_created(win, input):
    response_sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "response": {"start": 1.0, "stop": 7.0, "keys": ["space"]},
        },
    )

    correct_response_sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "response": {
                "start": 1.0,
                "stop": 7.0,
                "keys": ["space", "enter"],
                "variable": {"correct_key": "correct_key"},
            },
        },
    )

    assert type(response_sequence.response) == ResponseComponent
    assert type(correct_response_sequence.response) == CorrectResponseComponent


def test_no_response_infinity_duration(win, input, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "TestSequence",
                "visual_components": [{"name": "Text", "type": "TextStim", "spec": {}}],
            },
        )

    assert "TestSequence: Sequence has no way to finish" in capsys.readouterr().out


def test_not_cut_on_response_infinity_duration(
    win, input, capsys: pytest.CaptureFixture
):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "TestSequence",
                "visual_components": [{"name": "Text", "type": "TextStim", "spec": {}}],
                "response": {"keys": ["space"]},
            },
        )

    assert "TestSequence: Sequence has no way to finish" in capsys.readouterr().out


def test_cut_on_response_infinity_duration(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "cut_on_response": True,
            "visual_components": [{"name": "Text", "type": "TextStim", "spec": {}}],
            "response": {"keys": ["space"]},
        },
    )

    assert sequence._get_duration() == INFINITY


def test_wait_on_response_infinity_duration(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "cut_on_response": True,
            "wait_for_response": True,
            "visual_components": [{"name": "Text", "type": "TextStim", "spec": {}}],
            "response": {"keys": ["space"]},
        },
    )

    assert sequence._get_duration() == INFINITY


def test_finite_duration_wait_on_nonexisting_response(
    win, input, capsys: pytest.CaptureFixture
):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "TestSequence",
                "cut_on_response": True,
                "wait_for_response": True,
                "visual_components": [
                    {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
                ],
            },
        )

    assert "TestSequence: Sequence has no way to finish" in capsys.readouterr().out


def test_finite_duration_wait_on_nonexisting_response_but_infinity_timed(
    win, input, capsys: pytest.CaptureFixture
):
    with pytest.raises(SystemExit):
        Sequence(
            win,
            input,
            {
                "name": "TestSequence",
                "cut_on_response": True,
                "wait_for_response": True,
                "timed": True,
                "timer": INFINITY,
                "visual_components": [
                    {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
                ],
            },
        )

    assert "TestSequence: Sequence has no way to finish" in capsys.readouterr().out


def test_finite_duration_wait_on_nonexisting_response_but_timed(win, input):
    Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "cut_on_response": True,
            "wait_for_response": True,
            "timed": True,
            "timer": 30.0,
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
            ],
        },
    )


def test_finite_duration(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 3.0}
            ],
        },
    )

    assert sequence._get_duration() == 3.0


def test_finite_duration_with_timer(win, input):
    sequence1 = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "timed": True,
            "timer": 5.0,
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 3.0}
            ],
        },
    )

    sequence2 = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "timed": True,
            "timer": 5.0,
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 18.0}
            ],
        },
    )

    assert sequence1._get_duration() == 5.0
    assert sequence2._get_duration() == 5.0


def test_ininity_timer_changes_duration(win, input):
    sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "cut_on_response": True,
            "timed": True,
            "timer": INFINITY,
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 5.0}
            ],
            "response": {"keys": ["space"]},
        },
    )

    assert sequence._get_duration() == INFINITY


def test_refresh(sequence: Sequence):
    def get_diff() -> float:
        return sequence.clock.getTime() - sequence.input_device.device.clock.getTime()

    before_refresh = get_diff()
    sequence.refresh()
    after_refresh = get_diff()

    assert not before_refresh == pytest.approx(0.0, abs=0.0001)
    assert after_refresh == pytest.approx(0.0, abs=0.0001)


def test_run_frame(sequence: Sequence):
    sequence.refresh()

    text = sequence.visual[0]
    assert text.not_started()
    assert text.time_started == None
    assert text.time_started_flip == None
    assert text.time_started_global_flip == None

    seq_time = sequence.clock.getTime()
    seq_flip = sequence.window.getFutureFlipTime(clock=sequence.clock)
    win_flip = sequence.window.getFutureFlipTime()

    status = sequence._run_frame()

    assert status == 1
    assert text.started()
    assert text.time_started == pytest.approx(seq_time, abs=0.0001)
    assert text.time_started_flip == pytest.approx(seq_flip, abs=0.0001)
    assert text.time_started_global_flip == pytest.approx(win_flip, abs=0.0001)


def test_sequence_run(sequence: Sequence):
    text = sequence.visual[0]
    win_refresh = 1.2 / sequence.window.getActualFrameRate()

    text_stop_time = text.stop_time
    win_stop_time = sequence.window.getFutureFlipTime() + text_stop_time

    sequence.run()

    assert text.finished()
    assert text.time_stopped == pytest.approx(text_stop_time, abs=win_refresh)
    assert text.time_stopped_flip == pytest.approx(text_stop_time, abs=win_refresh)
    assert text.time_stopped_global_flip == pytest.approx(
        win_stop_time, abs=win_refresh * 2
    )
