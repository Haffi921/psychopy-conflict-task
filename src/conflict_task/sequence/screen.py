from .sequence import Sequence, DEFAULT_SEQUENCE_SETTINGS

DEFAULT_SCREEN_SETTINGS = {
    **DEFAULT_SEQUENCE_SETTINGS,
    "wait_for_response": True,
    "cut_on_response": True,
}


class Screen(Sequence):

    name: str = "Screen"

    def _parse_sequence_settings(
        self, sequence_settings, default_settings=DEFAULT_SCREEN_SETTINGS
    ):
        super()._parse_sequence_settings(
            sequence_settings, default_settings=default_settings
        )
