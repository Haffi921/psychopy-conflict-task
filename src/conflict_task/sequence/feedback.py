from conflict_task.devices import Window
from conflict_task.util import get_or_fatal_exit, true_or_fatal_exit

from .sequence import DEFAULT_SEQUENCE_SETTINGS, Sequence

DEFAULT_FEEDBACK_SETTINGS = {
    **DEFAULT_SEQUENCE_SETTINGS,
    "takes_trial_values": True,
}


class Feedback(Sequence):

    name: str = "Feedback"

    def __init__(self, sequence_settings: dict) -> None:
        self.feedback_function: function = None
        self.win_color = Window._window.color
        super().__init__(sequence_settings)

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
            Window._window.color = win_color

        super()._prepare_components(feedback_values)

    def run(self, trial_values: dict, allow_escape) -> None:
        feedback_success = super().run(
            trial_values=trial_values, allow_escape=allow_escape
        )
        Window._window.color = self.win_color
        return feedback_success
