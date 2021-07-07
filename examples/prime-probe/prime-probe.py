import sys
from os.path import dirname, realpath

sys.path.append(dirname(dirname(dirname(realpath(__file__)))))

from conflict_task.experiment import Experiment
from settings.experiment_settings import *
from settings.device_settings import *

prime_probe = Experiment(experiment_settings, window_settings, input_device)

prime_probe.run()