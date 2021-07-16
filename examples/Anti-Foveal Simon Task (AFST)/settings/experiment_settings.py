from .device_settings import *
from .trial_settings import *

experiment_settings = dict(
    blocks = dict(
        number = 1,
        trials = dict(
            number = 2,
            visualComponents = [fixation_cross, circle, target],
            response = response,
        )
    ),
    window_settings = window_settings,
    input_device = input_device,
)