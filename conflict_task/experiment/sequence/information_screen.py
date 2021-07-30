from conflict_task.experiment.sequence.choice_trial import ChoiceTrial
from psychopy import logging, core

from .base_sequence import BaseSequence
from ..component import ResponseComponent

class InformationScreen(ChoiceTrial):
    def __init__(self, window, input_device, data_handler, componentSettings):
        super().__init__(window, input_device, data_handler, componentSettings)

        self.wait_for_response = True
        self.cut_on_response = True