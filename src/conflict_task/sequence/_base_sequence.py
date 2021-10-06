from functools import reduce

from psychopy import clock

from conflict_task.component import *
from conflict_task.constants import *
from conflict_task.devices import InputDevice, Keyboard, Window
from conflict_task.util import *


class BaseSequence:
    def __init__(
        self, window: Window, input_device: InputDevice, sequence_settings: dict
    ) -> None:
        self._base_sequence_should_not_be_run()

        self.name: str = "unnamed_sequence"

        # Devices
        self.window: Window = window
        self.input_device: Keyboard = input_device

        # Components
        self.response: ResponseComponent = None
        self.visual: list[VisualComponent] = []
        self.audio: list[AudioComponent] = []
        self.wait: list[WaitComponent] = []

        # Clock
        self.clock: clock.Clock = clock.Clock()

        # Sequence settings
        self.variable_factor: dict = None
        self.timed: bool = False
        self.timer: float = 0.0
        self.wait_for_response: bool = False
        self.cut_on_response: bool = False
        self.takes_trial_values: bool = False
        self.feedback: bool = False

        self._parse_component_settings(sequence_settings)
        self._parse_sequence_settings(sequence_settings)

        if (
            not self.response or not self.cut_on_response
        ) and self._get_duration() == INFINITY:
            fatal_exit("Sequence has no way to finish.")

    def _base_sequence_should_not_be_run(self) -> None:
        if self.__class__.__name__ == "BaseSequence":
            fatal_exit("An instance of BaseSequence should not be created nor run")

    # ===============================================
    # Dictionary parsing
    # ===============================================
    def _parse_sequence_settings(
        self, sequence_settings: dict, default_settings: dict
    ) -> None:
        self._base_sequence_should_not_be_run()

        if name := get_type(sequence_settings, "name", str):
            self.name = name

        def retrieve_valid_settings(settings, nextKey) -> dict:
            if nextKey in sequence_settings:
                test_or_fatal_exit(
                    type(default_settings[nextKey]) == type(sequence_settings[nextKey]),
                    f"{self.name} - '{nextKey}' setting must be of type {default_settings[nextKey]}",
                )
                settings[nextKey] = sequence_settings[nextKey]

        settings: dict = default_settings | reduce(
            retrieve_valid_settings, default_settings.keys(), {}
        )

        for key, value in settings.items():
            setattr(self, key, value)

        if self.timed:
            self.timer = get_type_or_fatal_exit(
                sequence_settings,
                "timer",
                float,
                "If sequence is timed, please provide a timer",
            )

        """for key in default_settings.keys():
            if key in sequence_settings:
                settings[key] = sequence_settings[key]"""

        # settings = default_settings | settings

    def _parse_component_settings(self, sequence_settings: dict) -> None:
        self._base_sequence_should_not_be_run()

        if visual_components := sequence_settings.get("visual_components"):
            self.visual = self._create_components(
                visual_components, VisualComponent, self.window
            )

        if audio_components := sequence_settings.get("audio_components"):
            self.audio = self._create_components(
                audio_components, AudioComponent, self.window
            )

        if wait_components := sequence_settings.get("wait_components"):
            self.wait = self._create_components(wait_components, WaitComponent)

        if response := get_type(sequence_settings, "response", dict):
            if "correct_key" in get_type(response, "variable", dict, {}):
                self.response = CorrectResponseComponent(response)
            else:
                self.response = ResponseComponent(response)

    # ===============================================
    # Helper functions
    # ===============================================
    def _create_components(
        self, component_settings: dict, component_class: BaseComponent, *args, **kwargs
    ) -> BaseComponent:
        self._base_sequence_should_not_be_run()

        settings: list = None
        components: list = []

        if isinstance(component_settings, list):
            settings = component_settings
        elif isinstance(component_settings, dict):
            settings = list(component_settings.values())
        else:
            fatal_exit(
                f"Sequence components must listed either in a dictionary or as a list"
            )

        for component in settings:
            components.append(component_class(component, *args, **kwargs))

        return components

    def _get_all_components(self) -> list[BaseComponent]:
        self._base_sequence_should_not_be_run()

        return [
            self.response,
            *self.visual,
            *self.audio,
            *self.wait,
        ]

    def _get_duration(self) -> float:
        self._base_sequence_should_not_be_run()

        if self.timed:
            return self.timer

        return max(
            [
                component.stop_time
                for component in self._get_all_components()
                if component is not None
            ]
        )

    def _get_all_components_variable_factors(self) -> dict:
        self._base_sequence_should_not_be_run()

        def merge_variable_factors(
            variable_factors: dict, nextComponent: BaseComponent
        ):
            return variable_factors | nextComponent.variable_factor

        return reduce(merge_variable_factors, self._get_all_components(), {})

    # ===============================================
    # Sequence execution functions
    # ===============================================
    def _refresh(self) -> None:
        self._base_sequence_should_not_be_run()

        for component in self._get_all_components():
            component.refresh()

    def _prepare_components(self, trial_values: dict) -> None:
        self._base_sequence_should_not_be_run()

        for component in self._get_all_components():
            component.prepare(trial_values)

    def _run_frame(self, allow_escape=False) -> None:
        self._base_sequence_should_not_be_run()

        # Check if user wants to quit experiment
        if allow_escape and self.input_device.was_key_pressed("escape"):
            return QUIT_EXPERIMENT

        # Get current timers
        time = self.clock.getTime()
        thisFlip = self.window.getFutureFlipTime(clock=self.clock)
        thisFlipGlobal = self.window.getFutureFlipTime(clock=None)

        # Return variable is whether or not to continue the sequence
        keep_running = STOP_RUNNING

        # Iterate through components
        for component in self._get_all_components():

            # Either start them...
            if component.not_started():
                if thisFlip >= component.start_time - FRAMETOLERANCE:
                    component.start(time, thisFlip, thisFlipGlobal)
            # ...or stop them
            elif component.started():
                if thisFlip >= component.stop_time - FRAMETOLERANCE:
                    component.stop(time, thisFlip, thisFlipGlobal)

            # If not all components have finished, continue the sequence
            if not component.finished():
                keep_running = KEEP_RUNNING

        # If sequence has a response component check for it
        if self.response:
            self.response.check(self.input_device)

            # Two possibilities based on the response settings
            if self.response.made:
                if self.cut_on_response:
                    # Cutting sequence short after a response has been made
                    keep_running = STOP_RUNNING
            else:
                if self.wait_for_response:
                    # Wait for response even though all components have finished
                    keep_running = KEEP_RUNNING

        # Finally, if timed check if sequence has finished it's timer
        if self.timed:
            if thisFlip >= self.timer:
                keep_running = STOP_RUNNING

        # Flip window
        self.window.flip()

        # Continue sequence or not
        return keep_running

    # ===============================================
    # Public member functions
    # ===============================================
    def run(self, trial_values: dict = {}, allow_escape=False) -> None:
        self._base_sequence_should_not_be_run()

        self._refresh()
        if self.takes_trial_values:
            self._prepare_components(trial_values)

        self.clock.reset(-self.window.getFutureFlipTime(clock="now"))
        self.input_device.reset_clock()

        running = KEEP_RUNNING

        while running == KEEP_RUNNING:
            running = self._run_frame(allow_escape=allow_escape)

            if running == QUIT_EXPERIMENT:
                return False

        return True

    def get_data(self, prepend_key=True) -> dict:
        self._base_sequence_should_not_be_run()

        def merge_data(data: dict, nextComponent: BaseComponent):
            return data | nextComponent.get_data(prepend_key=prepend_key)

        data = reduce(merge_data, self._get_all_components(), {})

        if prepend_key:
            data = {f"{self.name}.{key}": value for key, value in data.items()}

        return data
