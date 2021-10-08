import pytest

from conflict_task.component._base_component import BaseComponent
from conflict_task.constants import *


def assert_component_has_settings(component: BaseComponent, settings: dict):
    for key, value in settings.items():
        assert hasattr(component, key)
        assert getattr(component, key) == value


def test_base_component_should_not_create(capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        BaseComponent({})

    assert (
        "An instance of BaseComponent should not be created nor run"
        in capsys.readouterr().out
    )


@pytest.mark.parametrize("component", [{}], indirect=True)
def test_new_component_default(component: BaseComponent, default_settings: dict):
    assert_component_has_settings(component, default_settings)


def test_start_stop_refresh(component: BaseComponent, default_settings: dict):
    # Start
    start_time_values = [1.0, 1.05, 15.05]
    started_settings = {
        **default_settings,
        "status": STARTED,
        "time_started": start_time_values[0],
        "time_started_flip": start_time_values[1],
        "time_started_global_flip": start_time_values[2],
    }

    component.start(*start_time_values)

    assert not component.not_started()
    assert component.started()
    assert not component.finished()

    assert_component_has_settings(component, started_settings)

    # Stop
    stop_time_values = [4.0, 4.02, 19.02]
    stopped_settings = {
        **started_settings,
        "status": FINISHED,
        "time_stopped": stop_time_values[0],
        "time_stopped_flip": stop_time_values[1],
        "time_stopped_global_flip": stop_time_values[2],
    }

    component.stop(*stop_time_values)

    assert not component.not_started()
    assert not component.started()
    assert component.finished()

    assert_component_has_settings(component, stopped_settings)

    # Refresh
    component.refresh()

    assert component.not_started()
    assert not component.started()
    assert not component.finished()

    assert_component_has_settings(component, default_settings)


@pytest.mark.parametrize(
    "component",
    [{"start": 1.0, "stop": 4.0, "variable": {"factor_name": "factor_id"}}],
    indirect=True,
)
def test_all_settings_are_set(component: BaseComponent, default_settings):
    print(component.get_data())
    assert_component_has_settings(
        component,
        {
            **default_settings,
            "start_time": 1.0,
            "stop_time": 4.0,
            "variable_factor": {"factor_name": "factor_id"},
        },
    )


@pytest.mark.parametrize("component", [{"start": 1.0, "duration": 4.0}], indirect=True)
def test_duration_setting(component):
    assert_component_has_settings(
        component,
        {
            "start_time": 1.0,
            "stop_time": 5.0,
        },
    )


def test_start_time_less_than_zero_fail(new_component, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        new_component({"start": -5.0})

    assert (
        "UNKNOWN_COMPONENT - Component start time can not be less than 0.0"
        in capsys.readouterr().out
    )


def test_stop_time_less_than_start_time_fail(
    new_component, capsys: pytest.CaptureFixture
):
    with pytest.raises(SystemExit):
        new_component({"start": 1.0, "stop": 0.5})

    assert (
        "UNKNOWN_COMPONENT - Component stop time must not be less than the start time"
        in capsys.readouterr().out
    )


@pytest.mark.parametrize("component", [{}], indirect=True)
def test_prepare_component_does_nothing_if_no_variable_factor(component: BaseComponent):
    component.prepare({"factor_id": "factor_value"})

    assert not hasattr(component, "factor_id")


@pytest.mark.parametrize(
    "component", [{"variable": {"factor_name": "factor_id"}}], indirect=True
)
def test_prepare_component(component: BaseComponent):
    component.prepare({"factor_id": "factor_value"})

    assert getattr(component, "factor_name") == "factor_value"


@pytest.mark.parametrize(
    "component", [{"variable": {"factor_name": "factor_id"}}], indirect=True
)
def test_prepare_component_fail(
    component: BaseComponent, capsys: pytest.CaptureFixture
):
    with pytest.raises(SystemExit):
        component.prepare({"another_factor_id": "another_factor_value"})

    assert (
        "Subject trial sequence does not include key 'factor_id' required by UNKNOWN_COMPONENT"
        in capsys.readouterr().out
    )
