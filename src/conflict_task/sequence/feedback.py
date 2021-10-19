from conflict_task.devices import InputDevice, Window
from conflict_task.util import get_or_fatal_exit, true_or_fatal_exit

from .sequence import Sequence

DEFAULT_FEEDBACK_SETTINGS = {
    "wait_for_response": False,
    "cut_on_response": False,
    "timed": False,
    "takes_trial_values": True,
}


class Feedback(Sequence):

    name: str = "Feedback"

    def __init__(
        self, window: Window, input_device: InputDevice, sequence_settings: dict
    ) -> None:
        self.feedback_function: function = None
        self.win_color = window.color
        super().__init__(window, input_device, sequence_settings)

    def _parse_sequence_settings(
        self,
        sequence_settings: dict,
        default_settings: dict = DEFAULT_FEEDBACK_SETTINGS,
    ):
        super()._parse_sequence_settings(
            sequence_settings, default_settings=default_settings
        )
        self.feedback_function = get_or_fatal_exit(
            sequence_settings,
            "trial_values",
            "Feedback must have 'trial_values' setting",
        )
        true_or_fatal_exit(
            callable(self.feedback_function),
            "Feedback 'trial_values' setting must be a function",
        )

    def _prepare_components(self, trial_values: dict) -> None:
        feedback_values: dict = self.feedback_function(trial_values)

        if win_color := feedback_values.get("win_color"):
            self.window.color = win_color

        super()._prepare_components(feedback_values)

    def run(self, trial_values: dict, allow_escape) -> None:
        feedback_success = super().run(
            trial_values=trial_values, allow_escape=allow_escape
        )
        self.window.color = self.win_color
        return feedback_success
