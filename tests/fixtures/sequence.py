import pytest

from conflict_task.sequence import Sequence


@pytest.fixture(scope="session")
def sequence(win, input) -> Sequence:
    sequence = Sequence(
        win,
        input,
        {
            "name": "TestSequence",
            "visual_components": [
                {"name": "Text", "type": "TextStim", "spec": {}, "stop": 0.3}
            ],
        },
    )
    return sequence
