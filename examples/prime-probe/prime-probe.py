from conflict_task.experiment import Experiment

from settings.experiment_settings import *
from sequence_creator import subject_sequence

prime_probe = Experiment("Prime-Probe", subject_sequence, experiment_settings)

prime_probe.run()