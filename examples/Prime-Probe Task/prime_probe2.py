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

DataHandler.start_participant_data(EXPERIMENT_NAME, subject_info={"age": "", "gender": ""})

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

window = Window()
input_device = Keyboard()
EMGConnector.connect()


def quit():
    window.flip()
    window.close()
    core.quit()


pre_trial = list(map(lambda screen: Screen(window, input_device, screen), pre_trial))
trial = Trial(window, input_device, trial_sequence)
between = Screen(window, input_device, between_blocks)
post_trial = Screen(window, input_device, post_trial)

practice_block_trial = Block(window, input_device, {"trial": trial, "post": between })
block_trial = Block(window, input_device, {"trial": trial, "between": between, "post": post_trial })

for pre in pre_trial:
    continue_experiment = pre.run()

    DataHandler.add_data_dict_and_next_entry(pre.get_data())

    if not continue_experiment:
        quit()

practice_block_trial.run(NR_PRACTICE_BLOCKS, NR_PRACTICE_TRIALS, practice_values, { "trial_block": "practice" })
block_trial.run(NR_BLOCKS, NR_TRIALS, experiment_values, { "trial_block": "block" })