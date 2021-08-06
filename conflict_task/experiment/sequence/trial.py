from conflict_task.constants import *

from . import BaseSequence, Feedback

class Trial(BaseSequence):
    feedback: Feedback = None

    def __init__(self, window, input_device, data_handler, componentSettings):
        super().__init__(window, input_device, data_handler, componentSettings)

        if "feedback" in componentSettings:
            self.feedback: Feedback = Feedback(window, input_device, data_handler, componentSettings["feedback"])
            self.feedback_variables = componentSettings["feedback"]["variable"]
        
    
    def run(self, trial_values: dict, debug_data = False):
        self.refresh()
        self.prepare_components(trial_values)

        self.data_handler.add_data_dict(trial_values)
        self.clock.reset(-self.window.getFutureFlipTime(clock="now"))

        running = KEEP_RUNNING
        
        while running == KEEP_RUNNING:
            running = self.run_frame(debug_data)

            if running == QUIT_EXPERIMENT:
                return False
        

        if self.feedback:
            feedback_values = {}
            for factor in self.feedback_variables:
                if hasattr(self, factor):
                    feedback_values[factor] = getattr(self, factor)
            self.feedback.prepare_components(feedback_values)
            self.feedback.clock.reset(-self.window.getFutureFlipTime(clock="now"))

            running = KEEP_RUNNING

            while running:
                running = self.feedback.run_frame(debug_data)

                if running == QUIT_EXPERIMENT:
                    return False
        
        self.data_handler.next_entry()
        
        return True