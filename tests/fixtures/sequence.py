import pytest

from conflict_task.devices.window import Window
from conflict_task.sequence import Screen
from conflict_task.sequence.sequence import Sequence


@pytest.fixture(scope="session")
def sequence(win, input, settings=None) -> Sequence:
    if settings is None:
        settings = {
            "name": "TestSequence",
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 0.3}
            ],
        }
    sequence = Sequence(
        win,
        input,
        settings,
    )
    return sequence


@pytest.fixture(
    scope="session",
    params=[
        {
            "settings": None,
            "win_setting": None,
        },
    ],
)
def screen(win, input, request) -> Screen:
    settings = request.param.get("settings")
    if settings is None:
        settings = {
            "name": "TestScreen",
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {"text": "Hello"}, "stop": 0.0}
            ],
            "response": {"keys": ["space"]},
        }
    if (win_setting := request.param.get("win_setting")) is not None:
        win = Window(win_setting)
    screen = Screen(
        win,
        input,
        settings,
    )
    return screen
