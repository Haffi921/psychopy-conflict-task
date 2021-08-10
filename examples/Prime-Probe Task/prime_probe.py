from conflict_task.experiment import Experiment, preview_component

from settings.experiment_settings import experiment_settings
from trial_values import trial_values


prime_probe = Experiment("Prime-Probe", trial_values, experiment_settings)

prime_probe.run()