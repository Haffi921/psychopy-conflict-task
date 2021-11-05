from conflict_task.block import Block
from conflict_task.devices.input_device import InputDevice
from conflict_task.devices.window import Window
from conflict_task.util.error import true_or_fatal_exit


class BlockExperiment:
    def __init__(
        self, win: Window, input_device: InputDevice, experiment_settings: dict
    ) -> None:
        self.win = (win,)
        self.input_device = (input_device,)

        self.practice_block = None
        self.nr_practice_blocks = 0
        self.nr_practice_trials = None

        self.trial_block = None
        self.nr_blocks = 0
        self.nr_trials = None

        self._parse_experiment_settings(experiment_settings)

    def _parse_experiment_settings(self, experiment_settings: dict):
        if practice := experiment_settings.get("practice_block"):
            self.practice_block = Block(self.win, self.input_device, practice)

        self.trial_block = Block(
            self.win, self.input_device, experiment_settings.get("trial_block")
        )

    def run(self, practice_trial_values: list = [], trial_values: list = []):
        if self.practice_block:
            self.practice_block.run(practice_trial_values, {"trial_block": "practice"})

        self.trial_block.run(trial_values, {"trial_block": "trial"})
