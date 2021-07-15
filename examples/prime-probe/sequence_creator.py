from conflict_task.util import counterbalance, Randomizer

from settings.experiment_settings import *

nr_blocks = experiment_settings["blocks"]["number"]
nr_trials = experiment_settings["blocks"]["trials"]["number"]

conditions = {
    "distractor": [
        ["Left\nLeft\nLeft", "Right\nRight\nRight"],
        ["Up\nUp\nUp", "Down\nDown\nDown"],
    ],
    "target": [
        ["Left", "Right"],
        ["Up", "Down"],
    ],
    "correct_resp": [
        ["a", "d"],
        ["j", "l"]
    ]
}

def translate(trial):
    hand, distractor, target = trial
    return {
        "hand": hand,
        "congruency": int(distractor != target),
        "distractor_text": conditions["distractor"][hand][distractor],
        "target_text": conditions["target"][hand][target],
        "correct_resp": conditions["correct_resp"][hand][target]
    }

rand = Randomizer(0, 1)
subject_sequence = []
for block in range(experiment_settings["blocks"]["number"]):
    sequence = counterbalance(
        trials = 2, factor_levels = [2, 2], levels = 2,
        alternating = True, alternator_start = rand.new_one(), Force=True
    )

    sequence = list(map(translate, sequence))
    subject_sequence.append(sequence)