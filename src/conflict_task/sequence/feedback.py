from conflict_task.devices import Window
from conflict_task.util import get_type_or_fatal_exit

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
        feedback_values_base = get_type_or_fatal_exit(
            sequence_settings,
            "feedback_values",
            dict,
            "Feedback must have 'feedback_values' setting",
        )

        self.feedback_values = {}
        self.feedback_values_dynamic = {}

        for value in feedback_values_base:
            if callable(feedback_values_base[value]):
                self.feedback_values_dynamic[value] = feedback_values_base[value]
            else:
                self.feedback_values[value] = feedback_values_base[value]

    def _prepare_components(self, trial_values: dict) -> None:
        for key, func in self.feedback_values_dynamic.items():
            self.feedback_values[key] = func(trial_values)

        if win_color := self.feedback_values.get("win_color"):
            Window._window.color = win_color

        super()._prepare_components(self.feedback_values)

    def run(self, trial_values: dict, allow_escape) -> None:
        feedback_success = super().run(
            trial_values=trial_values, allow_escape=allow_escape
        )
        Window._window.color = self.win_color
        return feedback_success
