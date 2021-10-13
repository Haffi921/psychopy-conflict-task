from __future__ import annotations

from functools import reduce

from psychopy import clock

from conflict_task.component import *
from conflict_task.constants import (
    FRAMETOLERANCE,
    INFINITY,
    KEEP_RUNNING,
    QUIT_EXPERIMENT,
    STOP_RUNNING,
)
from conflict_task.devices import InputDevice, Keyboard, Window
from conflict_task.util import (
    fatal_exit,
    get_type,
    get_type_or_fatal_exit,
    true_or_fatal_exit,
)


class BaseSequence:
    name: str = "UNKNOWN_SEQUENCE"

    def __init__(
        self, window: Window, input_device: InputDevice, sequence_settings: dict
    ) -> None:
        self._base_sequence_should_not_be_run()

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
        self.timer: float = None
        self.wait_for_response: bool = False
        self.cut_on_response: bool = False
        self.takes_trial_values: bool = False
        self.feedback: bool = False

        self._parse_sequence_settings(sequence_settings)
        self._parse_component_settings(sequence_settings)

        true_or_fatal_exit(
            self._get_all_components() != [], f"{self.name}: Sequence has no components"
        )

        true_or_fatal_exit(
            (self.response and self.cut_on_response)
            or (
                self._get_duration() != INFINITY
                and not (self.wait_for_response and not self.response)
            )
            or (self.timed and self.timer != INFINITY),
            f"{self.name}: Sequence has no way to finish",
        )

    def _base_sequence_should_not_be_run(self) -> None:
        if self.__class__.__name__ == "BaseSequence":
            fatal_exit("An instance of BaseSequence should not be created nor run")

    # ===============================================
    # Dictionary parsing
    # ===============================================
    def _parse_sequence_settings(
        self, sequence_settings: dict, default_settings: dict = {}
    ) -> None:
        self._base_sequence_should_not_be_run()

        if name := get_type(sequence_settings, "name", str):
            self.name = name

        def retrieve_valid_settings(settings, next_key) -> dict:
            if next_key in sequence_settings:
                true_or_fatal_exit(
                    type(default_settings[next_key])
                    == type(sequence_settings[next_key]),
                    f"{self.name}: '{next_key}' setting must be of type {default_settings[next_key]}",
                )
                settings[next_key] = sequence_settings[next_key]
            return settings

        settings: dict = {
            **default_settings,
            **reduce(retrieve_valid_settings, default_settings.keys(), {}),
        }

        for key, value in settings.items():
            setattr(self, key, value)

        if self.timed:
            self.timer = get_type_or_fatal_exit(
                sequence_settings,
                "timer",
                float,
                f"{self.name}: If sequence is timed, please provide a timer",
            )
            true_or_fatal_exit(
                self.timer > 0.0, f"{self.name}: Timer has to be greater than 0.0"
            )

    def _parse_component_settings(self, sequence_settings: dict) -> None:
        self._base_sequence_should_not_be_run()

        if visual_components := get_type(sequence_settings, "visual_components", list):
            self.visual = self._create_components(
                visual_components, VisualComponent, self.window
            )

        if audio_components := get_type(sequence_settings, "audio_components", list):
            self.audio = self._create_components(
                audio_components, AudioComponent, self.window
            )

        if wait_components := get_type(sequence_settings, "wait_components", list):
            self.wait = self._create_components(wait_components, WaitComponent)

        if (response := get_type(sequence_settings, "response", dict)) is not None:
            if "correct_key" in get_type(response, "variable", dict, {}):
                self.response = CorrectResponseComponent(response)
            else:
                self.response = ResponseComponent(response)

    # ===============================================
    # Helper functions
    # ===============================================
    def _create_components(
        self, component_settings: list, component_class: BaseComponent, *args, **kwargs
    ) -> BaseComponent:
        self._base_sequence_should_not_be_run()

        components: list = []

        true_or_fatal_exit(
            all(isinstance(component, dict) for component in component_settings),
            f"{self.name}: Components settings need to be a dictionary",
        )

        for component in component_settings:
            components.append(component_class(component, *args, **kwargs))

        return components

    def _get_all_components(self) -> list[BaseComponent]:
        self._base_sequence_should_not_be_run()

        return [
            component
            for component in [
                self.response,
                *self.visual,
                *self.audio,
                *self.wait,
            ]
            if component is not None
        ]

    def _stop_all_components(
        self, time: float, time_flip: float, global_flip: float
    ) -> None:
        self._base_sequence_should_not_be_run()

        for component in self._get_all_components():
            if component.started():
                component.stop(time, time_flip, global_flip)

    def _get_duration(self) -> float:
        self._base_sequence_should_not_be_run()

        duration = max(
            [component.stop_time for component in self._get_all_components()]
        )

        if self.timed and self.timed < duration:
            return self.timer
        return duration

    def reset_clock(self, new_t):
        self.clock.reset(newT=new_t)

    # ===============================================
    # Sequence execution functions
    # ===============================================
    def _refresh_components(self) -> None:
        self._base_sequence_should_not_be_run()

        for component in self._get_all_components():
            component.refresh()

    def _prepare_components(self, trial_values: dict) -> None:
        self._base_sequence_should_not_be_run()

        if self.takes_trial_values:
            for component in self._get_all_components():
                component.prepare(trial_values)

    def refresh(self, new_t: float = 0.0) -> None:
        self._base_sequence_should_not_be_run()

        self.reset_clock(new_t=new_t)
        self.input_device.reset_clock(new_t=new_t)

    def _run_frame(self, allow_escape=False) -> None:
        self._base_sequence_should_not_be_run()

        # Check if user wants to quit experiment
        if allow_escape and self.input_device.was_key_pressed("escape"):
            return QUIT_EXPERIMENT

        # Get current timers
        time = self.clock.getTime()
        time_flip = self.window.getFutureFlipTime(clock=self.clock)
        time_global_flip = self.window.getFutureFlipTime(clock=None)

        # Return variable is whether or not to continue the sequence
        keep_running = STOP_RUNNING

        # Iterate through components
        for component in self._get_all_components():

            # Either start them...
            if (
                component.not_started()
                and time_flip >= component.start_time - FRAMETOLERANCE
            ):
                component.start(time, time_flip, time_global_flip)
            # ...or stop them
            elif (
                component.started()
                and time_flip >= component.stop_time - FRAMETOLERANCE
            ):
                component.stop(time, time_flip, time_global_flip)

            # If not all components have finished, continue the sequence
            if not component.finished():
                keep_running = KEEP_RUNNING

        # If sequence has a response component check for it
        if self.response:
            self.response.check(self.input_device)

            # Two possibilities based on the response settings
            if self.response.made and self.cut_on_response:
                # Cutting sequence short after a response has been made
                keep_running = STOP_RUNNING
            elif self.wait_for_response:
                # Wait for response even though all components have finished
                keep_running = KEEP_RUNNING

        # Finally, if timed check if sequence has finished it's timer
        if self.timed and time_flip >= self.timer:
            keep_running = STOP_RUNNING
            self._stop_all_components(time, time_flip, time_global_flip)

        # Flip window
        self.window.flip()

        if keep_running == STOP_RUNNING:
            self._stop_all_components(time, time_flip, time_global_flip)

        # Continue sequence or not
        return keep_running

    # ===============================================
    # Public member functions
    # ===============================================
    def run(self, trial_values: dict = {}, allow_escape=False) -> None:
        self._base_sequence_should_not_be_run()

        self._refresh_components()
        self._prepare_components(trial_values)
        self.refresh(new_t=-self.window.getFutureFlipTime(clock="now"))

        running = KEEP_RUNNING

        while running == KEEP_RUNNING:
            running = self._run_frame(allow_escape=allow_escape)

            if running == QUIT_EXPERIMENT:
                return False

        return True

    def get_data(self, prepend_key=True) -> dict:
        self._base_sequence_should_not_be_run()

        def merge_data(data: dict, next_component: BaseComponent):
            return {**data, **next_component.get_data(prepend_key=prepend_key)}

        data = reduce(merge_data, self._get_all_components(), {})

        if prepend_key:
            data = {f"{self.name}.{key}": value for key, value in data.items()}

        return data
