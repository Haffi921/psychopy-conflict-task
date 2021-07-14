from numpy.random import randint
from counterbalancer import counterbalance

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

def constraint(sequence, item):
    if len(sequence) == 1:
        return True
    elif len(sequence) == 2:
        if sequence[-1][1] + item[1]:
            return False
        if sequence[-1][2] + item[2]:
            return False
    if sequence[-2][1] + sequence[-1][1] + item[1]:
        return False
    if sequence[-2][2] + sequence[-1][2] + item[2]:
        return False
    return True

sequence = counterbalance(trials = 128, factor_levels = [2, 2], levels = 2, alternating = True, alternator_start = randint(2), constraint_function=constraint)

def translate(trial):
    hand, distractor, target = trial
    return {
        "congruency": int(distractor != target),
        "distractor": conditions["distractor"][hand][distractor],
        "target": conditions["target"][hand][target],
        "correct response": conditions["correct_response"][hand][target]
    }

results = map(translate, sequence)

for r in results:
    print(r)