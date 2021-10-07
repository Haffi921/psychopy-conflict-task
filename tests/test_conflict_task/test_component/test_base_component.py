import pytest

from conflict_task.component._base_component import BaseComponent
from conflict_task.constants import *


class TestBaseComponent:
    class BaseDerivative(BaseComponent):
        pass

    component: BaseDerivative = BaseDerivative({})

    default_data = {
        "status": NOT_STARTED,
        "time_started": None,
        "time_started_flip": None,
        "time_started_global_flip": None,
        "time_stopped": None,
        "time_stopped_flip": None,
        "time_stopped_global_flip": None,
    }

    default_settings = {
        "name": "UNKNOWN_COMPONENT",
        "component": component,
        "variable_factor": None,
        "start_time": 0.0,
        "stop_time": INFINITY,
        **default_data,
    }

    def restart(self, settings=None):
        if settings is None:
            settings = self.default_settings
        self.component = self.BaseDerivative(settings)

        self.default_settings["component"] = self.component

    def assert_component_has_settings(self, settings: dict):
        for key, value in settings.items():
            assert hasattr(self.component, key)
            assert getattr(self.component, key) == value

    def test_not_started(self):
        self.assert_component_has_settings(self.default_settings)

    def test_start_stop_refresh(self):
        # Start
        start_time_values = [1.0, 1.05, 15.05]
        started_settings = {
            **self.default_settings,
            "status": STARTED,
            "time_started": start_time_values[0],
            "time_started_flip": start_time_values[1],
            "time_started_global_flip": start_time_values[2],
        }

        self.component.start(*start_time_values)

        assert not self.component.not_started()
        assert self.component.started()
        assert not self.component.finished()

        self.assert_component_has_settings(started_settings)

        # Stop
        stop_time_values = [4.0, 4.02, 19.02]
        stopped_settings = {
            **started_settings,
            "status": FINISHED,
            "time_stopped": stop_time_values[0],
            "time_stopped_flip": stop_time_values[1],
            "time_stopped_global_flip": stop_time_values[2],
        }

        self.component.stop(*stop_time_values)

        assert not self.component.not_started()
        assert not self.component.started()
        assert self.component.finished()

        self.assert_component_has_settings(stopped_settings)

        # Refresh
        self.component.refresh()

        assert self.component.not_started()
        assert not self.component.started()
        assert not self.component.finished()

        self.assert_component_has_settings(self.default_settings)

    def test_base_component_should_not_create(self, capsys: pytest.CaptureFixture):
        with pytest.raises(SystemExit):
            BaseComponent({})

        assert (
            "An instance of BaseComponent should not be created nor run"
            in capsys.readouterr().out
        )

    def test_all_settings_are_set(self):
        self.restart(
            {"start": 1.0, "stop": 4.0, "variable": {"factor_name": "factor_id"}}
        )

        self.assert_component_has_settings(
            {
                **self.default_settings,
                "start_time": 1.0,
                "stop_time": 4.0,
                "variable_factor": {"factor_name": "factor_id"},
            },
        )

    def test_duration_setting(self):
        self.restart(
            {
                "start": 1.0,
                "duration": 4.0,
            }
        )

        self.assert_component_has_settings(
            {
                "start_time": 1.0,
                "stop_time": 5.0,
            },
        )

    def test_start_time_less_than_zero_fail(self, capsys: pytest.CaptureFixture):
        with pytest.raises(SystemExit):
            self.restart({"start": -5.0})

        assert (
            "UNKNOWN_COMPONENT - Component start time can not be less than 0.0"
            in capsys.readouterr().out
        )

    def test_stop_time_less_than_start_time_fail(self, capsys: pytest.CaptureFixture):
        with pytest.raises(SystemExit):
            self.restart({"start": 1.0, "stop": 0.5})

        assert (
            "UNKNOWN_COMPONENT - Component stop time must not be less than the start time"
            in capsys.readouterr().out
        )

    def test_prepare_component_does_nothing_if_no_variable_factor(self):
        self.restart()

        self.component.prepare({"factor_id": "factor_value"})

        assert not hasattr(self.component, "factor_id")

    def test_prepare_component(self):
        self.restart({"variable": {"factor_name": "factor_id"}})

        self.component.prepare({"factor_id": "factor_value"})

        assert getattr(self.component, "factor_name") == "factor_value"

    def test_prepare_component_fail(self, capsys: pytest.CaptureFixture):
        self.restart({"variable": {"factor_name": "factor_id"}})

        with pytest.raises(SystemExit):
            self.component.prepare({"another_factor_id": "another_factor_value"})

        assert (
            "Subject trial sequence does not include key 'factor_id' required by UNKNOWN_COMPONENT"
            in capsys.readouterr().out
        )
