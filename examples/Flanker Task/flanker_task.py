from conflict_task.experiment import Experiment

from settings.experiment_settings import *
from sequence_creator import subject_sequence

flanker_task = Experiment("Flanker Task", subject_sequence, experiment_settings)

flanker_task.run()