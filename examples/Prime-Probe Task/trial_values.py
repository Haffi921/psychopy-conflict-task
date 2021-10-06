from settings.experiment_settings import *

from sequencing_helpers import Randomizer, counterbalance

conditions = {
    "distractor": [
        ["Left\nLeft\nLeft", "Right\nRight\nRight"],
        ["Up\nUp\nUp", "Down\nDown\nDown"],
    ],
    "target": [
        ["Left", "Right"],
        ["Up", "Down"],
    ],
    "correct_key": [["a", "d"], ["j", "l"]],
}


def translate(trial):
    hand, distractor, target = trial
    return {
        "hand": hand,
        "congruency": int(distractor != target),
        "distractor_text": conditions["distractor"][hand][distractor],
        "target_text": conditions["target"][hand][target],
        "correct_key": conditions["correct_key"][hand][target],
    }


rand = Randomizer(0, 1)
trial_values = []
for block in range(8):
    sequence = counterbalance(
        trials=128,
        factor_levels=[2, 2],
        levels=2,
        alternating=True,
        alternator_start=rand.new_one(),
    )

    sequence = list(map(translate, sequence))
    trial_values.append(sequence)
