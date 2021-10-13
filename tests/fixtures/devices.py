import pytest

from conflict_task.devices.input_device import Keyboard
from conflict_task.devices.window import Window


@pytest.fixture(scope="session")
def win() -> Window:
    win = Window({"fullscr": False, "size": (1, 1)})
    yield win
    win.close()


@pytest.fixture(scope="session")
def input() -> Keyboard:
    input = Keyboard()
    return input
