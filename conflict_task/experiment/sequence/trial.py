from . import BaseSequence

class Trial(BaseSequence):
    def __init__(self, window, input_device, data_handler, componentSettings, cut_on_response = False, wait_for_response = False):
        super().__init__(window, input_device, data_handler, componentSettings)
        
        self.cut_on_response = cut_on_response
        self.wait_for_response = wait_for_response