from conflict_task.experiment import Experiment
from trial_values import get_trial_values
from sequences.between_blocks import between_blocks
from sequences.post_trial import post_trial
from sequences.pre_trial import pre_trial
from sequences.trial import trial_sequence


EXPERIMENT_NAME = "Prime-Probe"

NR_PRACTICE_BLOCKS = 1
NR_PRACTICE_TRIALS = 24
NR_BLOCKS = 8
NR_TRIALS = 97

# experiment_settings = {
#     "name": "Prime-Probe",
#     "extra_info": {
#         "age": "",
#         "gender": ""
#     },
#     "sequences": {
#         "pre": pre_trial,
#         "trial": trial_sequence,
#         "between_blocks": between_blocks,
#         "post": post_trial,
#         "nr_blocks": NR_BLOCKS,
#         "nr_trials": NR_TRIALS,
#         "nr_practice_blocks": NR_PRACTICE_BLOCKS,
#         "nr_practice_trials": NR_TRIALS,
#     },
#     "marker": [50, 60],
#     "debug": True,
# }

# experiment = Experiment(experiment_settings)

# p_nr = experiment.data_handler.participant_number

# trial_values = [
#     *get_trial_values(NR_PRACTICE_TRIALS, NR_PRACTICE_BLOCKS, p_nr, True, Force=True),
#     *get_trial_values(NR_TRIALS, NR_BLOCKS, p_nr, add_initial_trial=True),
# ]

# experiment.validate_trial_values(trial_values)

#experiment.run()
from psychopy import core

from conflict_task.devices import DataHandler, EMGConnector, Keyboard, Window
from conflict_task.sequence import Screen, Trial

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


def emergency_quit():
    print("Aborting!")
    data_handler.abort()
    window.flip()
    window.close()
    core.quit()


def quit():
    data_handler.finish_participant_data()
    window.flip()
    window.close()
    core.quit()


pre_trial = list(map(lambda screen: Screen(window, input_device, screen), pre_trial))
trial = Trial(window, input_device, trial_sequence)
between = Screen(window, input_device, between_blocks)
post_trial = list(map(lambda screen: Screen(window, input_device, screen), post_trial))


experiment_data = {**data_handler.subject_info}

for pre in pre_trial:
    continue_experiment = pre.run()

    data_handler.add_data_dict_and_next_entry({**experiment_data, **pre.get_data()})

    if not continue_experiment:
        emergency_quit()

for practice_block_nr in range(NR_PRACTICE_BLOCKS):
    EMGConnector.send_marker(50, t=0.5, t_after=0.5)
    practice_block_data = {
        **experiment_data,
        "trial_block": "practice",
        "block": practice_block_nr + 1,
    }

    for trial_nr in range(NR_PRACTICE_TRIALS):
        trial_data = {**practice_block_data, "trial": trial_nr + 1}

        trial_values = {**trial_data, **practice_values[practice_block_nr][trial_nr]}

        continue_experiment = trial.run(trial_values=trial_values)

        data_handler.add_data_dict(trial_values)
        data_handler.add_data_dict_and_next_entry(trial.get_data())

        if not continue_experiment:
            emergency_quit()

    EMGConnector.send_marker(60, t=0.5)

    continue_experiment = between.run()

    data_handler.add_data_dict_and_next_entry(
        {**practice_block_data, **between.get_data()}
    )

    if not continue_experiment:
        emergency_quit()


for block_nr in range(NR_BLOCKS):
    block_data = {**experiment_data, "trial_block": "block", "block": block_nr + 1}

    if block_nr:
        continue_experiment = between.run()

        data_handler.add_data_dict_and_next_entry({**block_data, **between.get_data()})

        if not continue_experiment:
            emergency_quit()

    EMGConnector.send_marker(51 + block_nr, t=0.5, t_after=0.5)
    for trial_nr in range(NR_TRIALS):
        trial_data = {**block_data, "trial": trial_nr + 1}

        trial_values = {**trial_data, **experiment_values[block_nr][trial_nr]}

        continue_experiment = trial.run(trial_values=trial_values)

        data_handler.add_data_dict(trial_values)
        data_handler.add_data_dict_and_next_entry(trial.get_data())

        if not continue_experiment:
            emergency_quit()
    EMGConnector.send_marker(61 + block_nr, t=0.5)

for post in post_trial:
    post.run()

    data_handler.add_data_dict_and_next_entry({**experiment_data, **post.get_data()})

    if not continue_experiment:
        emergency_quit()

quit()