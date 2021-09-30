from .start_screen import *
from .components import *
from .between_blocks import *

experiment_settings = dict(
    experiment_sequence = dict(
        pre = [start_screen],
        block = dict(
            nr_blocks = 8,
            nr_trials = 128,
            trial = trial,
            between_blocks = between_blocks
        ),
        post = [start_screen]
    ),
    window_settings = dict(
        color = [-1, -1, -1],
    ),
    input_device = "Keyboard",
)