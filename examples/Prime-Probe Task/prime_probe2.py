from sequences.between_blocks import between_blocks
from sequences.post_trial import post_trial
from sequences.pre_trial import pre_trial
from sequences.trial import trial_sequence
from trial_values import get_trial_values

from conflict_task.block_experiment import BlockExperiment
from conflict_task.devices import DataHandler, EMGConnector, Keyboard, Window
from conflict_task.instructions import Instructions

EXPERIMENT_NAME = "Feedback"

NR_PRACTICE_BLOCKS = 1
NR_PRACTICE_TRIALS = 24
NR_BLOCKS = 8
NR_TRIALS = 97

DataHandler.start_participant_data(EXPERIMENT_NAME, dlg_info={"age": "", "gender": ""})

practice_values = get_trial_values(
    NR_PRACTICE_TRIALS,
    NR_PRACTICE_BLOCKS,
    DataHandler.get_participant_number(),
    practice=True,
    Force=True,
)
experiment_values = get_trial_values(
    NR_TRIALS, NR_BLOCKS, DataHandler.get_participant_number(), add_initial_trial=True
)

experiment_settings = {
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
}

window = Window()
input_device = Keyboard()
EMGConnector.connect()

instructions = Instructions(window, input_device, pre_trial)
experiment = BlockExperiment(window, input_device, experiment_settings)

instructions.run()
experiment.run(practice_values, experiment_values)
