import pytest
from numpy.core.fromnumeric import mean

from conflict_task.devices import Keyboard, Window
from conflict_task.sequence import Screen, Sequence, Trial, screen

win = Window({"color": [-1, -1, -1]})
win_refresh = 1.0 / win.getActualFrameRate()
input = Keyboard()


def xtest_screen():
    screen = Screen(
        win,
        input,
        {
            "name": "TestScreen",
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "spec": {
                        "text": "You need to press [space] to continue",
                        "height": 0.05,
                    },
                }
            ],
            "response": {"keys": ["space"]},
        },
    )

    text = screen.visual[0]
    response = screen.response
    global_flip = win.getFutureFlipTime()

    screen.run()

    assert text.finished()
    assert text.time_started < win_refresh
    assert text.time_started_flip < text.time_started + win_refresh
    assert text.time_started_global_flip < global_flip + win_refresh

    assert text.time_started == response.time_started
    assert text.time_started_flip == response.time_started_flip
    assert text.time_started_global_flip == response.time_started_global_flip
    assert text.time_stopped == response.time_stopped
    assert text.time_stopped_flip == response.time_stopped_flip
    assert text.time_stopped_global_flip == response.time_stopped_global_flip

    assert response.rt < text.time_stopped


def xtest_timed_screen():
    screen = Screen(
        win,
        input,
        {
            "name": "TestScreen",
            "timed": True,
            "timer": 2.0,
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "spec": {
                        "text": "This one is timed for 2 seconds, but you can still press [space] to quit early",
                        "height": 0.05,
                    },
                }
            ],
            "response": {"keys": ["space"]},
        },
    )

    text = screen.visual[0]
    response = screen.response

    screen.run()

    assert (
        text.time_stopped == pytest.approx(screen.timer, abs=win_refresh)
        or text.time_stopped == response.time_stopped
    )
    assert (
        text.time_stopped_flip == pytest.approx(screen.timer, abs=win_refresh)
        or text.time_stopped_flip == response.time_stopped_flip
    )


def xtest_timed_screen_no_response():
    screen = Screen(
        win,
        input,
        {
            "name": "TestScreen",
            "timed": True,
            "timer": 2.0,
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "spec": {
                        "text": "This one is timed for 2 seconds, you have to wait",
                        "height": 0.05,
                    },
                }
            ],
        },
    )

    text = screen.visual[0]

    screen.run()

    assert text.time_stopped == pytest.approx(screen.timer, abs=win_refresh)
    assert text.time_stopped_flip == pytest.approx(screen.timer, abs=win_refresh)


def xtest_timed_screen_non_cut_response():
    screen = Screen(
        win,
        input,
        {
            "name": "TestScreen",
            "timed": True,
            "timer": 2.0,
            "cut_on_response": False,
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "spec": {
                        "text": "This one is timed for 2 seconds, but you can still press [space]",
                        "height": 0.05,
                    },
                }
            ],
            "response": {"keys": ["space"]},
        },
    )
    screen.run()

    assert not screen.response.made or screen.response.rt < screen.timer


def test_trial_with_run():
    trial = Trial(
        win,
        input,
        {
            "type": "Trial",
            "takes_trial_values": True,
            "cut_on_response": True,
            "feedback": True,
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "stop": 1.0,
                    "spec": {"text": "This is a trial, press [space]", "height": 0.05},
                }
            ],
            "response": {"keys": ["space"], "stop": 1.0},
            "feedback_sequence": {
                "visual_components": [
                    {
                        "name": "text",
                        "type": "TextStim",
                        "stop": 1.0,
                        "spec": {
                            "height": 0.05,
                        },
                        "variable": {"text": "feedback_text"},
                    }
                ],
                "trial_values": lambda trial: {
                    "feedback_text": f"Your response time was {round(trial['rt'] * 1000)} ms"
                    if trial["made"]
                    else "No answer",
                },
            },
        },
    )

    lag = []
    for _ in range(10):
        trial.run()

        data = trial.get_data()
        """for k, v in data.items():
            print(f"{k}: {v}")"""
        text_start = data["Trial.response.time_started_global_flip"]
        response_time = data["Trial.response.rt"] or data["Trial.response.time_stopped"]
        feedback_start = data["Feedback.text.time_started_global_flip"]
        lag.append(feedback_start - text_start - response_time)

    print(lag)
    print(mean(lag))
    assert 0
