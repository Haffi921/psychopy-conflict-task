import pytest

from conflict_task.component._base_component import BaseComponent
from conflict_task.constants import *


class TestBaseComponent:
    class BaseDerivative(BaseComponent):
        pass

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
        "variable_factor": None,
        "start_time": 0.0,
        "stop_time": INFINITY,
        **default_data,
    }

    def compare_component_with_settings(self, component: BaseComponent, settings: dict):
        for key, value in settings.items():
            assert hasattr(component, key)
            assert getattr(component, key) == value

    def test_empty_class(self):
        component = self.BaseDerivative({})

        assert component.component == component
        self.compare_component_with_settings(component, self.default_settings)

    def test_start_stop_and_refresh(self):
        component = self.BaseDerivative({})

        # Not started
        not_started_settings = self.default_data

        assert component.not_started()
        assert not component.started()
        assert not component.finished()

        assert not_started_settings == component.get_data(prepend_key=False)

        # Started
        component.start(1.0, 1.05, 15.05)
        started_settings = {
            **not_started_settings,
            "status": STARTED,
            "time_started": 1.0,
            "time_started_flip": 1.05,
            "time_started_global_flip": 15.05,
        }

        assert not component.not_started()
        assert component.started()
        assert not component.finished()

        assert started_settings == component.get_data(prepend_key=False)

        # Finished
        component.stop(4.0, 4.02, 19.02)
        finished_settings = {
            **started_settings,
            "status": FINISHED,
            "time_stopped": 4.0,
            "time_stopped_flip": 4.02,
            "time_stopped_global_flip": 19.02,
        }

        assert not component.not_started()
        assert not component.started()
        assert component.finished()

        assert finished_settings == component.get_data(prepend_key=False)

        # Refresh
        component.refresh()

        assert component.not_started()
        assert not component.started()
        assert not component.finished()

        assert not_started_settings == component.get_data(prepend_key=False)

    def test_base_component_should_not_create(self, capsys: pytest.CaptureFixture):
        with pytest.raises(SystemExit):
            BaseComponent({})
        
        assert(
            "An instance of BaseComponent should not be created nor run"
            in capsys.readouterr().out
        )

    def test_all_settings_are_set(self):
        settings = {"start": 1.0, "stop": 4.0, "variable": {"factor_name": "factor_id"}}
        component = self.BaseDerivative(settings)

        assert component.component == component
        self.compare_component_with_settings(
            component,
            {
                **self.default_settings,
                "start_time": 1.0,
                "stop_time": 4.0,
                "variable_factor": {"factor_name": "factor_id"},
            },
        )

    def test_duration_setting(self):
        settings = {
            "start": 1.0,
            "duration": 4.0,
        }
        component = self.BaseDerivative(settings)

        self.compare_component_with_settings(
            component,
            {
                "start_time": 1.0,
                "stop_time": 5.0,
            },
        )

    def test_start_time_less_than_zero_fail(self, capsys: pytest.CaptureFixture):
        settings = {"start": -5.0}

        with pytest.raises(SystemExit):
            self.BaseDerivative(settings)

        assert(
            "UNKNOWN_COMPONENT - Component start time can not be less than 0.0"
            in capsys.readouterr().out
        )

    def test_stop_time_less_than_start_time_fail(self, capsys: pytest.CaptureFixture):
        settings = {"start": 1.0, "stop": 0.5}

        with pytest.raises(SystemExit):
            self.BaseDerivative(settings)
        
        assert(
            "UNKNOWN_COMPONENT - Component stop time must not be less than the start time"
            in capsys.readouterr().out
        )

    def test_prepare_component_does_nothing_if_no_variable_factor(self):
        component = self.BaseDerivative({})

        component.prepare({"factor_id": "factor_value"})

        assert not hasattr(component, "factor_id")

    def test_prepare_component(self):
        component = self.BaseDerivative({"variable": {"factor_name": "factor_id"}})

        component.prepare({"factor_id": "factor_value"})

        assert getattr(component, "factor_name") == "factor_value"

    def test_prepare_component_fail(self, capsys: pytest.CaptureFixture):
        component = self.BaseDerivative({"variable": {"factor_name": "factor_id"}})

        with pytest.raises(SystemExit):
            component.prepare({"another_factor_id": "another_factor_value"})

        assert (
            "Subject trial sequence does not include key 'factor_id' required by UNKNOWN_COMPONENT"
            in capsys.readouterr().out
        )
