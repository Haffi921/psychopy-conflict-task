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
    "correct_key": [
        ["f", "g"],
        ["j", "n"],
    ],
}


trial_values = []
for block in range(8):
    feedback_opacity = 1.0 if block < 4 else 0.0

    def translate(trial):
        hand, distractor, target = trial
        return {
            "hand": hand,
            "congruency": int(distractor != target),
            "distractor_text": conditions["distractor"][hand][distractor],
            "target_text": conditions["target"][hand][target],
            "correct_key": conditions["correct_key"][hand][target],
            "feedback_opacity": feedback_opacity,
        }

    sequence = counterbalance(
        trials=95, factor_levels=[2, 2], levels=2, alternating=True, Force=True
    )

    sequence = list(map(translate, sequence))
    trial_values.append(sequence)
