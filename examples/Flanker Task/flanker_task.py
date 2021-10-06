from sequence_creator import subject_sequence
from settings.experiment_settings import *

from conflict_task.experiment import Experiment

flanker_task = Experiment("Flanker Task", subject_sequence, experiment_settings)

flanker_task.run()
