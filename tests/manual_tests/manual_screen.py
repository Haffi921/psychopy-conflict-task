import pytest
from numpy.core.fromnumeric import mean

from conflict_task.devices import InputDevice, Window
from conflict_task.sequence import Screen, Sequence, Trial, screen

Window.start({"color": [0, 0, 0]})
win_refresh = 1.0 / Window.get_actual_framerate()


def xtest_screen():
    screen = Screen(
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
    global_flip = Window.get_future_flip_time()

    screen.run()

    assert text.finished()
    assert text.time_started <= win_refresh * 2
    assert text.time_started_flip <= text.time_started + win_refresh * 2
    assert text.time_started_global_flip <= global_flip + win_refresh * 2

    assert text.time_started == response.time_started
    assert text.time_started_flip == response.time_started_flip
    assert text.time_started_global_flip == response.time_started_global_flip
    assert text.time_stopped == response.time_stopped
    assert text.time_stopped_flip == response.time_stopped_flip
    assert text.time_stopped_global_flip == response.time_stopped_global_flip

    assert response.rt < text.time_stopped


def xtest_timed_screen():
    screen = Screen(
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


def xtest_trial_with_run():
    trial = Trial(
        {
            "type": "Trial",
            "takes_trial_values": True,
            "cut_on_response": True,
            "feedback": True,
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "start": 1.0,
                    "duration": 1.0,
                    "spec": {"text": "This is a trial, press [space]", "height": 0.05},
                }
            ],
            "response": {"keys": ["space"], "start": 1.0, "duration": 1.0},
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
                    "feedback_text": f"Your response time was {round((trial['response_rt'] - trial['response_start']) * 1000)} ms"
                    if trial["response_made"]
                    else "No answer",
                },
            },
        },
    )

    for _ in range(2):
        trial.run()


def xtest_trial_with_run_with_variable_feedback():
    trial = Trial(
        {
            "type": "Trial",
            "takes_trial_values": True,
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
            "variable": {"feedback": "feedback"},
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
                    "feedback_text": f"Your response time was {round(trial['response_rt'] * 1000)} ms"
                    if trial["response_made"]
                    else "No answer",
                },
            },
        },
    )

    trial_values = [
        {
            "feedback": True,
        },
        {
            "feedback": False,
        },
        {
            "feedback": True,
        },
        {
            "feedback": False,
        },
    ]

    for t in trial_values:
        trial.run(t)


def xtest_trial_with_correct_respone_feedback():
    trial = Trial(
        {
            "type": "Trial",
            "takes_trial_values": True,
            "cut_on_response": True,
            "feedback": True,
            "visual_components": [
                {
                    "name": "Text",
                    "type": "TextStim",
                    "start": 1.0,
                    "duration": 1.0,
                    "spec": {"height": 0.05},
                    "variable": {"text": "trial_text"},
                }
            ],
            "response": {
                "keys": ["a", "l"],
                "start": 1.0,
                "duration": 1.0,
                "variable": {"correct_key": "correct_key"},
            },
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
                    "feedback_text": "+"
                    if trial["response_made"] and trial["response_correct"]
                    else (
                        "Fehler!"
                        if trial["response_made"] and not trial["response_correct"]
                        else "Zu langsam"
                    ),
                    "win_color": "green"
                    if trial["response_made"] and trial["response_correct"]
                    else (
                        "red"
                        if trial["response_made"] and not trial["response_correct"]
                        else "black"
                    ),
                },
            },
        },
    )

    trial_values = [
        {
            "trial_text": "This is a trial, press [a] for correct",
            "correct_key": "a",
        },
        {
            "trial_text": "This is a trial, press [l] for incorrect",
            "correct_key": "a",
        },
    ]

    for t in trial_values:
        trial.run(t)
