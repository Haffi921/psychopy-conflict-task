from conflict_task.constants import *
from conflict_task.util import *

from .feedback import Feedback
from .sequence import DEFAULT_SEQUENCE_SETTINGS, Sequence

DEFAULT_TRIAL_SETTINGS = {
    **DEFAULT_SEQUENCE_SETTINGS,
    "takes_trial_values": True,
    "feedback": False,
}


class Trial(Sequence):

    name: str = "Trial"

    def __init__(self, sequence_settings: dict):
        self.variable_factor: dict = None

        self.feedback: bool = False
        self.feedback_sequence: Feedback = None

        super().__init__(sequence_settings)

        self._parse_feedback_settings(sequence_settings)

    def _parse_sequence_settings(
        self, sequence_settings, default_settings=DEFAULT_TRIAL_SETTINGS
    ):
        super()._parse_sequence_settings(sequence_settings, default_settings)

    def _parse_feedback_settings(self, sequence_settings: dict):
        feedback_settings = get_type(sequence_settings, "feedback_sequence", dict)

        if feedback_settings:
            self.feedback_sequence = Feedback(feedback_settings)
            true_or_fatal_exit(
                self.name != self.feedback_sequence.name,
                f"{self.name} - Trial and its feedback cannot have the same name",
            )

        elif self.feedback:
            fatal_exit(f"No settings found for feedback in trial: {self.name}")

    def run(self, trial_values: dict = {}, allow_escape=False):
        trial_success = super().run(
            trial_values=trial_values, allow_escape=allow_escape
        )

        if not trial_success:
            return trial_success

        if self.feedback:
            feedback_values = {**trial_values, **self.response.get_response_data()}

            feedback_success = self.feedback_sequence.run(
                trial_values=feedback_values, allow_escape=allow_escape
            )

        return trial_success and feedback_success

    def get_data(self, prepend_key: bool = True) -> dict:
        data = super().get_data(prepend_key=prepend_key)
        if self.feedback_sequence:
            data.update(self.feedback_sequence.get_data(prepend_key=prepend_key))
        return data
