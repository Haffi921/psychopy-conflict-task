from __future__ import annotations

from conflict_task.devices import EMGConnector, InputDevice
from conflict_task.util import *

from ._base_component import BaseComponent


class ResponseComponent(BaseComponent):
    """
    Component to record user input through an InputDevice.

    Records the key that a user responds with and the reaction time.
    """

    name = "response"

    def __init__(self, component_settings) -> None:
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

        ------------------------------------------

        ResponseComponent's settings must include:

            `keys`    (list): List of keys that users are allowed to responde with.
        """

        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------
        self.keys: list = None
        """List of keys that users are allowed to responde with."""

        self.made: bool = False
        """True if user has responded. Refreshes with `ResponseComponent.refresh()`."""

        self.key: str = None
        """The key that a user responds with. Refreshes with `ResponseComponent.refresh()`."""

        self.rt: float = None
        """The response time. Refreshes with `ResponseComponent.refresh()`."""
        # -----------------------------------------------

        # -----------------------------------------------
        # ResponseComponent Initialization
        # -----------------------------------------------
        super().__init__(component_settings)

        self.keys = get_type_or_fatal_exit(
            component_settings,
            "keys",
            list,
            "Response component - Must have a 'keys' setting",
        )
        true_or_fatal_exit(
            len(self.keys), "Response component - Setting 'keys' must include some keys"
        )
        true_or_fatal_exit(
            all(isinstance(key, str) for key in self.keys),
            "Response component - Keys specified in 'keys' must be strings",
        )
        # -----------------------------------------------

    def start(self, time, time_flip, global_flip) -> None:
        super().start(time, time_flip, global_flip)
        InputDevice.reset_events()

    def refresh(self) -> None:
        """
        Used before each component use.

        For all components, this refreshes `status`, `time_started`, `time_started_refresh`,
        `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.

        For a ResponseComponent, this refreshes variables `made`, `key` and `rt`.
        """

        super().refresh()

        self.made = False
        self.key = None
        self.rt = None

    def check(self) -> tuple[str, float]:
        """
        Checks for input using `input_device` and logs data using `data_handler`.

        Uses `ResponseComponent.keys` list as input possiblities. If user presses any of the keys from this list:

            1) `made` becomes True

            2) `key` and `rt` are recorded

        Args:

            `input_device`        (InputDevice): Device used to check input. Can be Keyboard or any Parallel port device.

        Returns:

            Keypress tuple (str, float): Tuple with key and reaction time.
        """

        if self.started() and not self.made:
            key_press = InputDevice.get_last_key(self.keys)

            if key_press is not None:
                self._process_response(key_press)
                self.send_marker_value()

                return key_press
        return (None, None)

    def get_response_data(self) -> dict:
        return {
            "response_start": self.time_started_flip,
            "response_made": self.made,
            "response_key": self.key,
            "response_rt": self.rt,
        }

    def _process_response(self, key_press) -> None:
        self.key, self.rt = key_press
        self.made = True


class CorrectResponseComponent(ResponseComponent):
    """
    Component to record user input through an InputDevice and compare to a correct response.

    Records the key that a user responds with, the reaction time and correctness.
    """

    def __init__(self, component_settings) -> None:
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

        ------------------------------------------

        ResponseComponent's settings must include:

            `keys`    (list): List of keys that users are allowed to responde with.

        ------------------------------------------

        CorrectResponseComponent's settings must have `correct_key` (str) as a variable factor.
        """

        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------
        self.correct_key: str = None
        """String of the correct repsonse key"""

        self.correct: bool = None
        """True if response key is correct"""

        self.marker_values: list = None
        # -----------------------------------------------

        super().__init__(component_settings)

        true_or_fatal_exit(
            get_type(self.variable_factor, "correct_key", str),
            "CorrectResponse component - 'correct_key' must be a key in variable factors",
        )

    def _parse_EMG_marker_settings(self, component_settings: dict) -> None:
        if EMGConnector.connected():
            self.marker_values = get_type(component_settings, "marker", list)
            if self.marker_values:
                true_or_fatal_exit(
                    all(isinstance(value, int) for value in self.marker_values),
                    f"{self.name}: Marker values must be integers. Values are {self.marker_values}",
                )
                true_or_fatal_exit(
                    len(self.marker_values) == 3,
                    f"{self.name}: Marker values must be exactly three for Correct (1), Incorrect (2), and No Response (3)",
                )
                true_or_fatal_exit(
                    all(0 <= value < 256 for value in self.marker_values),
                    f"{self.name}: Marker values must be in the range of 0-255. Values are {self.marker_values}",
                )

    def refresh(self) -> None:
        """
        Used before each component use.

        For all components, this refreshes `status`, `time_started`, `time_started_refresh`,
        `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.

        For a ResponseComponent, this refreshes variables `made`, `key` and `rt`.

        For a CorrectResponseComponent, this refreshes variables `correct_key` and `correct`.
        """

        super().refresh()

        self.correct_key = None
        self.correct = None
        self.marker_value = None

    def stop(self, time, time_flip, global_flip) -> None:
        super().stop(time, time_flip, global_flip)
        if self.marker_values and not self.made:
            self.marker_value = self.marker_values[2]
            self.send_marker_value()

    def check(self) -> tuple[str, float]:
        """
        Checks for input using `input_device` and logs data using `data_handler`. \n

        Uses `ResponseComponent.keys` list as input possiblities. If user presses any of the keys from this list:

            1) `made` becomes True.

            2) `key` and `rt` are recorded.

            3) `correct` becomes True if `key` == `correct_key`, and False if `key` != `correct_key`.

        Args:

            `input_device`        (InputDevice): Device used to check input. Can be Keyboard or any Parallel port device.
        """

        return super().check()

    def _process_response(self, key_press) -> None:
        super()._process_response(key_press)
        self.correct = self.key == self.correct_key
        if self.marker_values:
            self.marker_value = self.marker_values[int(not self.correct)]

    def get_response_data(self) -> dict:
        return {
            **super().get_response_data(),
            "response_correct_key": self.correct_key,
            "response_correct": self.correct,
        }
