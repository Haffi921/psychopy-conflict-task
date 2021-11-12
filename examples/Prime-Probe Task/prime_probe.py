from sequences.instructions import *
from sequences.trial import *
from trial_values import get_trial_values

from conflict_task.block_experiment import BlockExperiment

NR_PRACTICE_BLOCKS = 1
NR_PRACTICE_TRIALS = 24
NR_BLOCKS = 8
NR_TRIALS = 97

experiment_settings = {
    "name": "Feedback",
    "extra_info": {"age": "", "gender": ""},
    "instructions": instructions,
    "blocks": {
        "practice_block": {
            "trial": trial_sequence,
            "post": between_blocks,
            "nr_blocks": NR_PRACTICE_BLOCKS,
            "nr_trials": NR_PRACTICE_TRIALS,
            "marker": [50, 60],
        },
        "trial_block": {
            "trial": trial_sequence,
            "between": between_blocks,
            "post": post_trial,
            "nr_blocks": NR_BLOCKS,
            "nr_trials": NR_TRIALS,
            "marker": [51, 61],
        },
    },
    "marker": True,
}

experiment = BlockExperiment(experiment_settings)

practice_values = get_trial_values(
    NR_PRACTICE_TRIALS,
    NR_PRACTICE_BLOCKS,
    experiment.get_participant_number(),
    practice=True,
    force=True,
)

experiment_values = get_trial_values(
    NR_TRIALS, NR_BLOCKS, experiment.get_participant_number(), add_initial_trial=True
)

experiment.run(practice_values, experiment_values)
