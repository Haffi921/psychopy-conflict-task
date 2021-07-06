from trial_settings import *

experiment = dict(
    blocks = dict(
        number = 2,
        trials = dict(
            number = 5,
            components = [fixation_cross, distractor, target],
            response = response
        )
    )
)