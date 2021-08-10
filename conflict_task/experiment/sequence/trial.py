from psychopy import logging, core
from conflict_task.constants import *

from .sequence import Sequence
from .feedback import Feedback

DEFAULT_TRIAL_SETTINGS = {
    "wait_for_response": False,
    "cut_on_response": False,
    "timed": False,
    "takes_trial_values": True,
    "feedback": False
}

class Trial(Sequence):
    
    def __init__(self, window, input_device, data_handler, trial_settings):
        self.feedback: bool = False
        self.feedback_sequence: Feedback = None

        super().__init__(window, input_device, data_handler, trial_settings)

        if self.feedback:
            if "feedback" not in trial_settings:
                logging.fatal(f"No settings found for feedback in trial: {self.name}")
                core.quit()
            self.feedback_sequence = Feedback(window, input_device, data_handler, trial_settings["feedback"])

    
    def _parse_sequence_settings(self, sequence_settings, default_settings = DEFAULT_TRIAL_SETTINGS):
        return super()._parse_sequence_settings(sequence_settings, default_settings)

        # self.feedback: Feedback = None
        # if "feedback" in trial_settings:
        #     self.feedback: Feedback = Feedback(window, input_device, data_handler, trial_settings["feedback"])
        #     self.feedback_variables = trial_settings["feedback"]["variable"]
        
    
    # def run(self, trial_values: dict, debug_data = False):
    #     self.refresh()
    #     self.prepare_components(trial_values)

    #     self.data_handler.add_data_dict(trial_values)
    #     self.clock.reset(-self.window.getFutureFlipTime(clock="now"))

    #     running = KEEP_RUNNING
        
    #     while running == KEEP_RUNNING:
    #         running = self.run_frame(debug_data)

    #         if running == QUIT_EXPERIMENT:
    #             return False
        

    #     # if self.feedback:
    #     #     feedback_values = {}
    #     #     for factor in self.feedback_variables:
    #     #         if hasattr(self, factor):
    #     #             feedback_values[factor] = getattr(self, factor)
    #     #     self.feedback.prepare_components(feedback_values)
    #     #     self.feedback.clock.reset(-self.window.getFutureFlipTime(clock="now"))

    #     #     running = KEEP_RUNNING

    #     #     while running:
    #     #         running = self.feedback.run_frame(debug_data)

    #     #         if running == QUIT_EXPERIMENT:
    #     #             return False
        
    #     self.data_handler.next_entry()
        
    #     return True