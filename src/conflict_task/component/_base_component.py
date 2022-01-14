from conflict_task.constants import *
from conflict_task.devices.EMG_connector import EMGConnector
from conflict_task.util import *

BASECOMPONENT_DATA_EXCLUSION = [
    "component",
    "variable_factor",
]


class BaseComponent:
    name = "UNKNOWN_COMPONENT"
    """Name of component for data registration."""

    def __init__(self, component_settings: dict) -> None:
        """
        Takes in a `component_settings` dictionary to set up component variables.

        For all components, settings are as follows:

            1) `start`          (float): Start time for component relative to sequence start. Defaults to 0.0.

            2) End time, either through:
                a) `stop`       (float): Stop time for component relative to sequence start.
                b) `duration`   (float): Length of time between component's start and stop.
                Behind the scenes `stop` = `start` + `duration`.
                c) None, which means the component will be displayed indefinitely until the end of the sequence.

            3) `variable`        (dict): Component member variables that will be different each sequence.
        """

        self._base_component_should_not_be_run()

        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------

        self.component = self
        """Reference to an object that trial values modify. Default: `self`"""

        self.variable_factor: dict = None
        """Dictionary of component member variables that will be different each sequence. Default: `None`."""

        self.start_time: float = 0.0
        """Start time for component relative to sequence start. Default: `0.0`."""

        self.stop_time: float = INFINITY
        """Stop time for component relative to sequence start. Default:`Infinity`."""

        self.marker_value: int = None
        """EMG marker to send on stimulus onset"""

        self.status: int = NOT_STARTED
        """Component status (NOT_STARTED, STARTED, FINISHED). Defaults: `NOT_STARTED`."""

        self.time_started: float = None
        """Time that component started, relative to sequence start.Default: `None`."""

        self.time_started_flip: float = None
        """Screen flip time that component started, relative to sequence start.Default: `None`."""

        self.time_started_global_flip: float = None
        """Screen flip time that component started, relative to experiment start.Default: `None`."""

        self.time_stopped: float = None
        """Time that component stopped, relative to sequence start.Default: `None`."""

        self.time_stopped_flip: float = None
        """Screen flip time that component stopped, relative to sequence start.Default: `None`."""

        self.time_stopped_global_flip: float = None
        """Screen flip time that component stopped, relative to experiment start.Default: `None`."""
        # -----------------------------------------------

        # -----------------------------------------------
        # BaseComponent Initialization
        # -----------------------------------------------
        self.start_time = get_type(component_settings, "start", float, 0.0)
        if "stop" in component_settings:
            self.stop_time = get_type(component_settings, "stop", float)
        elif "duration" in component_settings:
            self.stop_time = self.start_time + get_type(
                component_settings, "duration", float
            )

        self.variable_factor = get_type(component_settings, "variable", dict)

        true_or_fatal_exit(
            self.start_time >= 0.0,
            f"{self.name} - Component start time can not be less than 0.0",
        )
        true_or_fatal_exit(
            self.stop_time >= self.start_time,
            f"{self.name} - Component stop time must not be less than the start time",
        )

        self._parse_EMG_marker_settings(component_settings)
        # -----------------------------------------------

    def send_marker_value(self) -> None:
        if self.marker_value:
            EMGConnector.send_marker(self.marker_value)

    def _parse_EMG_marker_settings(self, component_settings: dict) -> None:
        self._base_component_should_not_be_run()

        if EMGConnector.connected():
            self.marker_value = get_type(component_settings, "marker", int)
            if self.marker_value:
                true_or_fatal_exit(
                    0 < self.marker_value < 256,
                    f"{self.name}: Marker value must be in the range of 1-255. Value is {self.marker_value}",
                )

    def _base_component_should_not_be_run(self) -> None:
        true_or_fatal_exit(
            self.__class__.__name__ != "BaseComponent",
            "An instance of BaseComponent should not be created nor run",
        )

    def refresh(self) -> None:
        """
        Refreshes component variables. Perform before each component use.

        For all components, this refreshes `status`, `time_started`, `time_started_refresh`,
        `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.
        """

        self._base_component_should_not_be_run()

        self.status = NOT_STARTED
        self.time_started = None
        self.time_started_flip = None
        self.time_started_global_flip = None
        self.time_stopped = None
        self.time_stopped_flip = None
        self.time_stopped_global_flip = None

    def prepare(self, trial_values: dict) -> None:
        """
        Sets the key-value pairs from `trial_values` on the component.

        Args:

            `trial_values`   (dict): Dictionary of key-value pairs that link up component member variables (keys) with their respective values.

            `component`       (Any): The object on which the `trial_values` are enacted on. Defaults to `self`.
        """

        self._base_component_should_not_be_run()

        if self.variable_factor is not None:

            for factor_name, factor_id in self.variable_factor.items():
                true_or_fatal_exit(
                    factor_id in trial_values.keys(),
                    f"Subject trial sequence does not include key '{factor_id}' required by {self.name} component",
                )
                setattr(self.component, factor_name, trial_values[factor_id])

    def start(self, time, time_flip, global_flip) -> None:
        """
        Starts component and records time.

        Args:

            `time`        (float): Time relative to sequence start.

            `flipTime`    (float): Screen flip time relative to sequence start.

            `timeGlobal`  (float): Screen flip time relative to experiment start.
        """

        self._base_component_should_not_be_run()

        self.time_started = time
        self.time_started_flip = time_flip
        self.time_started_global_flip = global_flip
        self.status = STARTED

    def stop(self, time, time_flip, global_flip) -> None:
        """
        Stops component and records time.

        Args:

            `time`                     (float): Time relative to sequence start.

            `flipTime`                 (float): Screen flip time relative to sequence start.

            `timeGlobal`               (float): Screen flip time relative to experiment start.
        """

        self._base_component_should_not_be_run()

        self.time_stopped = time
        self.time_stopped_flip = time_flip
        self.time_stopped_global_flip = global_flip
        self.status = FINISHED

    def not_started(self) -> bool:
        """
        Returns True if component has not been started, false if not.
        """

        self._base_component_should_not_be_run()

        return self.status == NOT_STARTED

    def started(self) -> bool:
        """
        Returns True if component has been started, false if not.
        """

        self._base_component_should_not_be_run()

        return self.status == STARTED

    def finished(self) -> bool:
        """
        Returns True if component has finished, false if not.
        """

        self._base_component_should_not_be_run()

        return self.status == FINISHED

    def get_data(self, prepend_key: bool = True) -> dict:
        """
        Returns a dictionary of the component's data
        """
        self._base_component_should_not_be_run()

        variables = vars(self)

        data = {
            item: variables[item]
            for item in variables
            if item not in BASECOMPONENT_DATA_EXCLUSION
        }

        if prepend_key:
            data = {f"{self.name}.{key}": value for key, value in data.items()}

        return data
