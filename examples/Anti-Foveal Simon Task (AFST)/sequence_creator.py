from conflict_task.util import counterbalance, Randomizer

from settings.experiment_settings import *

nr_blocks = experiment_settings["blocks"]["number"]
nr_trials = experiment_settings["blocks"]["trials"]["number"]

conditions = {
    "target_text": ["Up", "Down"],
    "target_pos": [(0, 0.05), (0, -0.05), (-0.05, 0), (0.05, 0)],
    "correct_key": ["up", "down"]
}

def translate(trial):
    target_text, target_pos = trial
    if target_text == target_pos:
        congruency = "Congruent"
    elif target_pos in [2, 3]:
        congruency = "Neutral"
    else:
        congruency = "Incongruent"
    return {
        "congruency": congruency,
        "target_text": conditions["target_text"][target_text],
        "target_pos": conditions["target_pos"][target_pos],
        "correct_key": conditions["correct_key"][target_text]
    }

subject_sequence = []
for block in range(experiment_settings["blocks"]["number"]):
    sequence = counterbalance(trials = 64, factor_levels = [2, 4], levels = 1)

    sequence = list(map(translate, sequence))
    subject_sequence.append(sequence)