from .trial_settings import *

experiment_settings = dict(
    blocks = dict(
        number = 2,
        trials = dict(
            number = 5,
            visualComponents = [fixation_cross, distractor, target],
            response = response,
        )
    )
)