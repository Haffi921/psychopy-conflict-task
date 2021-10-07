import pytest

from conflict_task.devices.input_device import Keyboard
from conflict_task.devices.window import Window
from conflict_task.sequence._base_sequence import BaseSequence


class BaseDerivative(BaseSequence):
    pass


win = Window({"fullscr": False, "size": (1, 1)})
input_device = Keyboard()


def test_empty_sequence():
    pass


def test_all_sequence_settings_are_set():
    pass


def test_empty_sequence_settings_are_set():
    pass


def test_if_timed_and_timer_are_set():
    pass


def test_if_timer_is_not_set():
    pass


def test_if_timer_is_not_float():
    pass


def test_no_response_infinity_duration():
    pass


def test_not_cut_on_response_infinity_duration():
    pass


def test_finite_duration():
    pass


def test_finite_duration_with_timer():
    pass


def test_empty_component_settings():
    pass


def test_component_settings_not_lists():
    pass


def test_component_settings_work():
    pass


def test_correct_response_created():
    pass


def test_get_component_variable_factor():
    pass


def test_run():
    pass
