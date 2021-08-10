from .sequence import DEFAULT_SEQUENCE_SETTINGS, Sequence

SCREEN_SETTINGS = DEFAULT_SEQUENCE_SETTINGS | {
    "wait_for_response": True,
    "cut_on_response": True,
    "takes_trial_values": False
}

class Screen(Sequence):
    def __init__(self, window, input_device, data_handler, sequence_settings):
        super().__init__(window, input_device, data_handler, sequence_settings)
    
    def _parse_sequence_settings(self, sequence_settings, default_settings = SCREEN_SETTINGS):
        return super()._parse_sequence_settings(sequence_settings, default_settings)