from conflict_task.experiment import Experiment

from settings.experiment_settings import *
from sequence_creator import subject_sequence

afst_task = Experiment("Anti-Foveal Simon Task", subject_sequence, experiment_settings)

afst_task.run()

#Experiment.previewStim(window_settings, circle)