from ._base_sequence import BaseSequence

class Screen(BaseSequence):
    wait_for_response = True
    cut_on_response = True

    def __init__(self, window, input_device, data_handler, componentSettings):
        super().__init__(window, input_device, data_handler, componentSettings)