from conflict_task.constants import *
from conflict_task.util import *

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

    name: str = "trial"
    
    def __init__(self, window, input_device, sequence_settings):
        self.feedback: bool = False
        self.feedback_sequence: Feedback = None

        super().__init__(window, input_device, sequence_settings)

    
    def _parse_sequence_settings(self, sequence_settings, default_settings = DEFAULT_TRIAL_SETTINGS):
        super()._parse_sequence_settings(sequence_settings, default_settings)

        if self.feedback:
            feedback_settings = get_type_or_fatal_exit(sequence_settings, "feedback", dict,
                f"No settings found for feedback in trial: {self.name}"
            )
            self.feedback_sequence = Feedback(self.window, self.input_device, feedback_settings)
        
        test_or_fatal_exit(self.name != self.feedback_sequence.name,
            f"{self.name} - Trial and its feedback cannot have the same name"
        )
        
    
    def run(self, trial_values: dict = {}, allow_escape = False):
        super().run(trial_values=trial_values, allow_escape=allow_escape)

        trial_values = trial_values | self.get_data()

        self.feedback_sequence.run(trial_values=trial_values, allow_escape=allow_escape)
    

    def get_data(self) -> dict:
        return super().get_data() | self.feedback_sequence.get_data()