import pytest

from conflict_task.devices.window import Window
from conflict_task.sequence import Screen
from conflict_task.sequence.sequence import Sequence


@pytest.fixture(scope="session")
def sequence(win, input) -> Sequence:
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


def screen(win, input) -> Screen:
    settings = {
        "name": "TestScreen",
        "visual_components": [
            {"name": "Text", "type": "TextStim", "spec": {}, "stop": 0.3}
        ],
        "response": {"keys": ["space"]},
    }
    screen = Screen(
        win,
        input,
        settings,
    )
    return screen
