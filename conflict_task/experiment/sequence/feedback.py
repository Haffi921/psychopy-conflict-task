from .sequence import Sequence

class Feedback(Sequence):

    def __init__(self, window, input_device, data_handler, sequence_settings):
        super().__init__(window, input_device, data_handler, sequence_settings)