from numpy.random import randint
from counterbalancer import counterbalance

trials = 128
conditions = {
    "distractor": [
        ["Left\nLeft\nLeft", "Right\nRight\nRight"],
        ["Up\nUp\nUp", "Down\nDown\nDown"],
    ],
    "target": [
        ["Left", "Right"],
        ["Up", "Down"],
    ],
    "correct_response": [
        ["a", "d"],
        ["j", "l"]
    ]
}

sequence = counterbalance(trials, [2, 2], 2, True, randint(2))

def translate(trial):
    alternating, distractor, target = trial
    return {
        "congruency": 1 - int(distractor == target),
        "distractor": conditions["distractor"][alternating][distractor],
        "target": conditions["target"][alternating][target],
        "correct response": conditions["correct_response"][alternating][target]
    }

results = map(translate, sequence)

for trial in list(results):
    print(trial)