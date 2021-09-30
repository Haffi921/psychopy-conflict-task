from .sequence import Sequence

DEFAULT_FEEDBACK_SETTINGS = {
    "wait_for_response": False,
    "cut_on_response": False,
    "timed": False,
    "takes_trial_values": True,
}

class Feedback(Sequence):

    name: str = "feedback"

    def _parse_sequence_settings(self, sequence_settings: dict, default_settings: dict = DEFAULT_FEEDBACK_SETTINGS):
        super()._parse_sequence_settings(sequence_settings, default_settings=default_settings)