from psychopy import core

from conflict_task.block import Block
from conflict_task.devices import DataHandler, EMGConnector, Keyboard, Window
from conflict_task.sequence import Screen, Trial

from trial_values import get_trial_values
from sequences.between_blocks import between_blocks
from sequences.post_trial import post_trial
from sequences.pre_trial import pre_trial
from sequences.trial import trial_sequence

EXPERIMENT_NAME = "Feedback"

NR_PRACTICE_BLOCKS = 1
NR_PRACTICE_TRIALS = 24
NR_BLOCKS = 8
NR_TRIALS = 97

data_handler = DataHandler(EXPERIMENT_NAME, subject_info={"age": "", "gender": ""})
data_handler.start_participant_data()

practice_values = get_trial_values(
    NR_PRACTICE_TRIALS,
    NR_PRACTICE_BLOCKS,
    data_handler.get_participant_number(),
    practice=True,
    Force=True,
)
experiment_values = get_trial_values(
    NR_TRIALS, NR_BLOCKS, data_handler.get_participant_number(), add_initial_trial=True
)

window = Window()
input_device = Keyboard()
EMGConnector.connect()


def quit():
    data_handler.finish_participant_data()
    window.flip()
    window.close()
    core.quit()


pre_trial = list(map(lambda screen: Screen(window, input_device, screen), pre_trial))
trial = Trial(window, input_device, trial_sequence)
between = Screen(window, input_device, between_blocks)
post_trial = list(map(lambda screen: Screen(window, input_device, screen), post_trial))

practice_block_trial = Block(window, input_device, data_handler, trial, post_screen=between)
block_trial = Block(window, input_device, data_handler, trial, between, post_trial)

experiment_data = data_handler.subject_info

for pre in pre_trial:
    continue_experiment = pre.run()

    data_handler.add_data_dict_and_next_entry({**experiment_data, **pre.get_data()})

    if not continue_experiment:
        quit()

practice_block_trial.run(NR_PRACTICE_BLOCKS, NR_PRACTICE_TRIALS, practice_values, {{**experiment_data, "trial_block": "practice" }})
block_trial.run(NR_BLOCKS, NR_TRIALS, experiment_values, {{**experiment_data, "trial_block": "block" }})

quit()