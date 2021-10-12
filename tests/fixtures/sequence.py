import pytest

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


@pytest.fixture(scope="session")
def screen(win, input, settings=None) -> Screen:
    if settings is None:
        settings = {
            "name": "TestScreen",
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 0.0}
            ],
            "response": {"keys": ["space"]}
        }
    screen = Screen(
        win,
        input,
        settings,
    )
    return screen
