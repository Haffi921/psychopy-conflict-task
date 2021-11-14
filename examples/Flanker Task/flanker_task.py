from sequence_creator import subject_sequence
from settings.experiment_settings import *

from conflict_task.block_experiment import BlockExperiment

flanker_task = BlockExperiment("Flanker Task", subject_sequence, experiment_settings)

flanker_task.run()
