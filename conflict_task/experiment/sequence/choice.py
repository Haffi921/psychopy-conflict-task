from . import BaseSequence

class Choice(BaseSequence):
    def __init__(self, window, input_device, data_handler, componentSettings):
        super().__init__(window, input_device, data_handler, componentSettings)

        self.wait_for_response = True