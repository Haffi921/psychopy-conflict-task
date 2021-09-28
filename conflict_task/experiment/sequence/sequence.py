from psychopy import logging, core

from conflict_task.constants import *

from ._base_sequence import BaseSequence

DEFAULT_SEQUENCE_SETTINGS = {
    "wait_for_response": False,
    "cut_on_response": False,
    "timed": False,
}

class Sequence(BaseSequence):
    
    def __init__(self, window, input_device, data_handler, sequence_settings):
        super().__init__(window, input_device, data_handler, sequence_settings)

        settings: dict = self._parse_sequence_settings(sequence_settings)

        for key, value in settings.items():
            setattr(self, key, value)

        # Why is this not in BaseSequence?
        if self.timed:
            try:
                if "timer" in sequence_settings:
                    self.timer = float(sequence_settings["timer"])
                else:
                    raise ValueError("If sequence is timed, please provide a timer")
            except ValueError as e:
                logging.fatal(e)
                core.quit()
        
        if (not self.response or not self.cut_on_response) and self.get_duration() == INFINITY:
            logging.fatal("Sequence has no way to finish.")
            core.quit()

    def _parse_sequence_settings(self, sequence_settings: dict, default_settings: dict = DEFAULT_SEQUENCE_SETTINGS):
        settings = {}

        for key in default_settings.keys():
            if key in sequence_settings:
                settings[key] = sequence_settings[key]
        
        settings = default_settings | settings

        return settings