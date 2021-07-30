from psychopy import logging, core

from .base_sequence import BaseSequence
from ..component import CorrectResponseComponent

class CorrectTrial(BaseSequence):
    def __init__(self, window, input_device, data_handler, componentSettings, cut_on_response = False, wait_for_response = False):
        super().__init__(window, input_device, data_handler, componentSettings)

        if "correct_response" in componentSettings:
            self.response = CorrectResponseComponent(componentSettings["response"])
        else:
            logging.fatal("CorrectTrial must have a correct_response component")
            core.quit()
        
        self.cut_on_response = cut_on_response
        self.wait_for_response = wait_for_response