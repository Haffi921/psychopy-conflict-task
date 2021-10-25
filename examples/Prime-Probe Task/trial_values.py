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


def get_trial_values(
    nr_trials: int,
    nr_blocks: int,
    participant_number: int,
    practice=False,
    add_initial_trial=False,
    Force=False,
):
    trial_values = []
    for block in range(nr_blocks):
        participant_group = bool(participant_number % 2)
        feedback_block = (
            (participant_group if block < (nr_blocks / 2) else not participant_group)
            if not practice
            else True
        )
        practice_modifier = 70 if practice else 0

        def translate(trial):
            hand, distractor, target = trial

            # Markers
            marker_start = 1 + (distractor + (target * 2) + (hand * 4)) + practice_modifier
            marker_end = marker_start + 10

            return {
                # Data
                "hand": hand,
                "congruency": int(distractor != target),

                # Stim variables
                "distractor_text": conditions["distractor"][hand][distractor],
                "target_text": conditions["target"][hand][target],
                "correct_key": conditions["correct_key"][hand][target],
                "feedback_block": feedback_block,

                # Markers
                "marker_start": marker_start,
                "marker_end": marker_end,
            }

        sequence = counterbalance(
            trials=nr_trials - int(add_initial_trial),
            factor_levels=[2, 2],
            levels=1,
            alternating=True,
            add_initial_trial=add_initial_trial,
            Force=Force,
        )

        sequence = list(map(translate, sequence))
        trial_values.append(sequence)

    return trial_values
