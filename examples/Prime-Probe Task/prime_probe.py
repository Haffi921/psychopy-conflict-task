from sequences.between_blocks import between_blocks
from sequences.pre_trial import start_screen
from sequences.trial import trial
from trial_values import trial_values

from conflict_task.experiment import Experiment

experiment_settings = dict(
    name="Prime-Probe",
    allow_escape=True,
    experiment_sequence=dict(
        pre=[start_screen],
        block=dict(
            nr_blocks=8, nr_trials=96, trial=trial, between_blocks=between_blocks
        ),
        post=[start_screen],
    ),
)

prime_probe = Experiment(trial_values, experiment_settings)

prime_probe.run()
