import numpy as np
from numpy.random import choice

from conflict_task.util import Alternator

trials = 32

sequential_conditions = None

alternating_conditions = {
    "distractor": [
        ["Left\nLeft\nLeft", "Right\nRight\nRight"],
        ["Up\nUp\nUp", "Down\nDown\nDown"],
    ],
    "target": [
        ["Left", "Right"],
        ["Up", "Down"],
    ]
}

levels = 1

condition_keys = list(alternating_conditions.keys())
