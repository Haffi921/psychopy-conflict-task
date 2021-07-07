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

                if not continue_experiment:
                    break
            if not continue_experiment:
                break
        
        self.window.close()
        core.quit()

    # def run_block(self) -> bool:
    #     for _ in range(self.nr_trials):
    #         continue_experiment = self.run_trial()

    #         if not continue_experiment:
    #             return continue_experiment
        
    #     return True
    
    # def run_trial(self):
    #     self.trial.refresh()
    #     running = True
    #     t = 0
    #     self.trial.clock.reset(-self.window.getFutureFlipTime(clock="now"))

    #     while running:
    #         if self.input_device.getKeys(["escape"]):
    #             return False
            
    #         t = self.trial.clock.getTime()
    #         thisFlip = self.window.getFutureFlipTime(clock=self.trial.clock)
    #         thisFlipGlobal = self.window.getFutureFlipTime(clock=None)

    #         running = False

    #         for component in self.trial.get_components_and_response():
    #             if self.trial.component_not_started(component):
    #                 if thisFlip >= component.start - self._frameTolerance:
    #                     self.trial.start_component(component, t, thisFlipGlobal)
    #             elif self.trial.component_started(component):
    #                 if thisFlip >= component.stop - self._frameTolerance:
    #                     self.trial.stop_component(component, t, thisFlipGlobal)
                
    #             if not self.trial.component_finished(component):
    #                 running = True
            
    #         self.trial.check_response(self.input_device)

    #         self.window.flip()


