from settings.experiment_settings import *

from conflict_task.util import Randomizer, counterbalance

nr_blocks = experiment_settings["blocks"]["number"]
nr_trials = experiment_settings["blocks"]["trials"]["number"]

conditions = {
    "distractor_text": ["<< <<", ">> >>"],
    "target_text": ["<", ">"],
    "correct_key": ["left", "right"],
}


def translate(trial):
    distractor, target = trial

    distractor_text = conditions["distractor_text"][distractor]
    target_text = conditions["target_text"][target]
    correct_key = conditions["correct_key"][target]

    return {
        "congruency": int(distractor != target),
        "distractor_text": distractor_text,
        "target_text": target_text,
        "correct_key": correct_key,
    }


subject_sequence = []
for block in range(experiment_settings["blocks"]["number"]):
    sequence = counterbalance(trials=64, factor_levels=[2, 2], levels=2)

    sequence = list(map(translate, sequence))
    subject_sequence.append(sequence)
