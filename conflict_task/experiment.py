from window import Window

class Experiment:
    nr_blocks = 0
    nr_trials = 0
    trial_components = None
    response = None

    window = None
    input_device = None

    def __init__(self, experiment_settings, trial_settings, window_settings, input_device):
        self.window = Window(window_settings)
        self.input_device = input_device