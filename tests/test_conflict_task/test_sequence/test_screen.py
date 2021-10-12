import time

import pytest

from conflict_task.sequence.screen import Screen


def test_screen_settings(screen: Screen):
    assert screen.wait_for_response
    assert screen.cut_on_response


@pytest.mark.parametrize(
    "screen",
    [{"win_setting": {}}],
    indirect=["screen"],
)
def xtest_screen_run(screen: Screen):
    screen.run()
