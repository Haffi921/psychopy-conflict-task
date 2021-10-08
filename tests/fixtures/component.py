import pytest

from conflict_task.component._base_component import BaseComponent
from conflict_task.constants import *


class BaseDerivative(BaseComponent):
    def get_data(self, prepend_key: bool = True, data_exclusion: list = []) -> dict:
        """
        Returns a dictionary of the component's data
        """
        data = {item: vars(self)[item] for item in vars(self)}

        return data


_component: BaseDerivative = None
# current_settings: dict = None

default_component_settings = {
    "variable_factor": None,
    "start_time": 0.0,
    "stop_time": INFINITY,
}


@pytest.fixture
def component(request):
    global _component
    if not hasattr(request, "param"):
        return _component
    _component = BaseDerivative(request.param)
    return _component


@pytest.fixture
def new_component():
    def new(settings):
        global _component
        _component = BaseDerivative(settings)
        return _component

    return new


@pytest.fixture
def current_settings():
    return _component.get_data(prepend_key=False, data_exclusion=[])


@pytest.fixture
def default_data():
    return {
        "status": NOT_STARTED,
        "time_started": None,
        "time_started_flip": None,
        "time_started_global_flip": None,
        "time_stopped": None,
        "time_stopped_flip": None,
        "time_stopped_global_flip": None,
    }


@pytest.fixture
def default_settings(default_data):
    return {
        "name": "UNKNOWN_COMPONENT",
        "component": _component,
        **default_component_settings,
        **default_data,
    }
