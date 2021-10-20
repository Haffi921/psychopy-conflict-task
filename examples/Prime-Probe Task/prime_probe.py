from psychopy import core
from sequences.between_blocks import between_blocks
from sequences.pre_trial import start_screen
from sequences.trial import trial_sequence

from conflict_task.sequence import Screen, Trial
from conflict_task.devices import Window, Keyboard, DataHandler

# experiment_settings = dict(
#     name="Prime-Probe",
#     allow_escape=True,
#     experiment_sequence=dict(
#         pre=[start_screen],
#         block=dict(
#             nr_blocks=8, nr_trials=97, trial=trial, between_blocks=between_blocks
#         ),
#         post=[start_screen],
#     ),
# )

# prime_probe = Experiment(trial_values, experiment_settings)

# prime_probe.run()


EXPERIMENT_NAME = "Prime-Probe"
DEBUG = False

NR_BLOCKS = 8
NR_TRIALS = 96

from trial_values import get_trial_values

data_handler = DataHandler(EXPERIMENT_NAME)
data_handler.start_participant_data()

experiment_values = get_trial_values(NR_TRIALS, NR_BLOCKS, data_handler.get_participant_number())

window = Window()
input_device = Keyboard()

window.setMouseVisible(False)

def emergency_quit():
    data_handler.abort()
    window.flip()
    window.close()
    core.quit()

def quit():
    data_handler.finish_participant_data()
    window.flip()
    window.close()
    core.quit()

pre_screens = [Screen(window, input_device, start_screen)]
trial = Trial(window, input_device, trial_sequence)
between = Screen(window, input_device, between_blocks)
post_screens = [Screen(window, input_device, start_screen)]


experiment_data = {"experiment_name": EXPERIMENT_NAME}

for pre in pre_screens:
    continue_experiment = pre.run(allow_escape=True)

    data_handler.add_data_dict_and_next_entry({
        **experiment_data, **pre.get_data()
    })

    if not continue_experiment:
        emergency_quit()

for block_nr in range(NR_BLOCKS):
    block_data = {**experiment_data, "block": block_nr + 1}

    if block_nr:
        continue_experiment = between.run(allow_escape=DEBUG)

        data_handler.add_data_dict_and_next_entry(
            {**block_data, **between.get_data()}
        )

        if not continue_experiment:
            emergency_quit()
    
    for trial_nr in range(NR_TRIALS):
        trial_data = {**block_data, "trial": trial_nr + 1}

        trial_values = {**trial_data, **experiment_values[block_nr][trial_nr]}

        continue_experiment = trial.run(trial_values=trial_values, allow_escape=DEBUG)

        data_handler.add_data_dict(trial_values)
        data_handler.add_data_dict_and_next_entry(trial.get_data())

        if not continue_experiment:
            emergency_quit()

for post in post_screens:
    post.run(allow_escape=DEBUG)

    data_handler.add_data_dict_and_next_entry(
        {**experiment_data, **post.get_data()}
    )

    if not continue_experiment:
        emergency_quit()

quit()