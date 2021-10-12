import pytest

from conflict_task.devices.input_device import Keyboard
from conflict_task.devices.window import Window


@pytest.fixture(
    scope="session", params=[{"settings": {"fullscr": False, "size": (1, 1)}}]
)
def win(request) -> Window:
    win = Window(request.param["settings"])
    yield win
    win.close()


@pytest.fixture(scope="session")
def input() -> Keyboard:
    input = Keyboard()
    return input
