from sequencing_helpers import Randomizer, counterbalance

conditions = {
    "distractor": [
        ["Links\nLinks\nLinks", "Rechts\nRechts\nRechts"],
        ["Oben\nOben\nOben", "Unten\nUnten\nUnten"],
    ],
    "target": [
        ["Links", "Rechts"],
        ["Oben", "Unten"],
    ],
    "correct_key": [
        ["f", "g"],
        ["j", "n"],
    ],
}

def get_trial_values(nr_trials: int, nr_blocks: int, participant_number: int):
    trial_values = []
    for block in range(nr_blocks):
        participant_group = float(participant_number % 2)
        feedback_opacity = participant_group if block < (nr_blocks / 2) else float(1.0 - participant_group)

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
            trials=nr_trials, factor_levels=[2, 2], levels=1, alternating=True
        )

        sequence = list(map(translate, sequence))
        trial_values.append(sequence)

    return trial_values
