from .device_settings import *
from .trial_settings import *

experiment_settings = dict(
    blocks=dict(
        number=1,
        trials=dict(
            number=64,
            visualComponents=[fixation_cross, distractor, target],
            response=response,
        ),
    ),
    window_settings=window_settings,
    input_device=input_device,
)
