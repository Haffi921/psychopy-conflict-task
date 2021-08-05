from psychopy import logging, core

from ..sequence.base_sequence import BaseSequence

from ..component import ResponseComponent


class InformationScreen(BaseSequence):
    """
    Used to display experiment information to participants.

    InformationScreen is static and response-agnostic.
    """

    def __init__(self, window, input_device, data_handler, componentSettings):
        super().__init__(window, input_device, data_handler, componentSettings)

        if "response" in componentSettings:
            self.response = ResponseComponent(componentSettings["response"])
        else:
            logging.fatal("InformationScreens need a response component")
            core.quit()
        
        self.wait_for_response = True
        self.cut_on_response = True
            