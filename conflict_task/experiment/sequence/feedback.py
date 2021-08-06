from ._base_sequence import BaseSequence

class Feedback(BaseSequence):

    def __init__(self, window, input_device, data_handler, componentSettings):
        super().__init__(window, input_device, data_handler, componentSettings)