from ._base_sequence import BaseSequence

DEFAULT_SEQUENCE_SETTINGS = {
    "early_quit_keys": [],
    "wait_for_response": False,
    "cut_on_response": False,
    "timed": False,
    "marker": False,
}


class Sequence(BaseSequence):
    def _parse_sequence_settings(
        self,
        sequence_settings: dict,
        default_settings: dict = DEFAULT_SEQUENCE_SETTINGS,
    ):
        super()._parse_sequence_settings(sequence_settings, default_settings)
