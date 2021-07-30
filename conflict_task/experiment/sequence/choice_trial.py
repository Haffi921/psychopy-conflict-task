from psychopy import logging, core

from .base_sequence import BaseSequence
from ..component import ResponseComponent

class ChoiceTrial(BaseSequence):
    def __init__(self, window, input_device, data_handler, componentSettings, cut_on_response = False, wait_for_response = False):
        super().__init__(window, input_device, data_handler, componentSettings)

        if "response" in componentSettings:
            self.response = ResponseComponent(componentSettings["response"])
        else:
            logging.fatal("ChoiceTrial must have a response component")
            core.quit()

        self.cut_on_response = cut_on_response
        self.wait_for_response = wait_for_response