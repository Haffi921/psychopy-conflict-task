from sequence_creator import subject_sequence
from settings.experiment_settings import *

from conflict_task.experiment import Experiment

afst_task = Experiment("Anti-Foveal Simon Task", subject_sequence, experiment_settings)

afst_task.run()

# Experiment.previewStim(window_settings, circle)
