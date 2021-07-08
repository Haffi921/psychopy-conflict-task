from psychopy import core, clock
from .window import Window
from .trial import Trial

class Experiment:
    nr_blocks = 0
    nr_trials = 0
    trial = None

    window = None
    input_device = None

    clock = clock.Clock()
    _frameTolerance = 0.001

    def __init__(self, experiment_settings, window_settings, input_device):
        self.window = Window(window_settings)
        self.input_device = input_device

        self.nr_blocks = experiment_settings["blocks"]["number"]
        self.nr_trials = experiment_settings["blocks"]["trials"]["number"]

        visualComponents = experiment_settings["blocks"]["trials"]["visualComponents"]
        response = experiment_settings["blocks"]["trials"]["response"]

        self.trial = Trial(self.window, visualComponents, response)
        
    
    def run(self):
        continue_experiment = True

        for _ in range(self.nr_blocks):
            for _ in range(self.nr_trials):
                continue_experiment = self.trial.run(self.window, self.input_device, self._frameTolerance)
                
                if self.trial.target.alternating:
                    self.trial.alternator.next()

                if not continue_experiment:
                    break
            if not continue_experiment:
                break
        
        self.window.close()
        core.quit()

