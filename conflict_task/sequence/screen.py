from .sequence import Sequence

DEFAULT_SCREEN_SETTINGS = {
    "wait_for_response": True,
    "cut_on_response": True,
    "timed": False
}

class Screen(Sequence):

    name: str = "screen"
   
    def _parse_sequence_settings(self, sequence_settings, default_settings = DEFAULT_SCREEN_SETTINGS):
        super()._parse_sequence_settings(sequence_settings, default_settings=default_settings)