from __future__ import annotations

from conflict_task.devices import DataHandler, EMGConnector, InputDevice, Window
from conflict_task.sequence import Screen, Sequence, Trial
from conflict_task.util import get_or_fatal_exit, get_type


class Block:
    def __init__(self, block_settings: dict) -> None:
        self.nr_blocks: int = 0
        self.nr_trials: int = None
        self.marker: list = None

        self.trial: Trial = None
        self.between: list[Screen] = None
        self.post: list[Screen] = None

        self._parse_block_settings(block_settings)

    def _parse_block_settings(self, block_settings: dict):
        self.nr_blocks = get_type(block_settings, "nr_blocks", int)
        self.nr_trials = get_type(block_settings, "nr_trials", int)
        self.marker = get_type(block_settings, "marker", list)
        self._parse_sequence_settings(block_settings)

    def _parse_sequence_settings(self, block_settings: dict):
        self.trial = get_or_fatal_exit(
            block_settings, "trial", "Block settings must have 'trial' settings"
        )
        if not isinstance(self.trial, Trial):
            self.trial = Trial(self.trial)

        def produce_auxiliary_screen_lists(name: str):
            settings = block_settings.get(name)
            if settings:
                if not isinstance(settings, list):
                    settings = [settings]
                for i, s in enumerate(settings):
                    if not isinstance(s, Screen):
                        settings[i] = Screen(s)
            return settings

        self.between = produce_auxiliary_screen_lists("between")
        self.post = produce_auxiliary_screen_lists("post")

    def run_sequence(self, sequence: Sequence, trial_values={}, data={}):
        continue_experiment = sequence.run(trial_values)

        DataHandler.add_data_dict_and_next_entry(
            {
                **data,
                **sequence.get_data(),
                "post_response_keypresses": InputDevice.get_keys([]),
            }
        )

        if not continue_experiment:
            Window.quit()

    def run(self, trial_values_list: list[list[dict]] = [], experiment_data: dict = {}):
        for block in range(self.nr_blocks):
            block_data = {
                **experiment_data,
                "block": block + 1,
            }
            if self.between and block:
                for between in self.between:
                    self.run_sequence(between, data=block_data)

            if self.marker:
                EMGConnector.send_marker(self.marker[0] + block, t=0.5, t_after=0.5)

            for trial in range(self.nr_trials):
                trial_values = {
                    **block_data,
                    "trial": trial + 1,
                    **trial_values_list[block][trial],
                }

                self.run_sequence(
                    self.trial, trial_values=trial_values, data=trial_values
                )

            if self.marker:
                EMGConnector.send_marker(self.marker[1] + block, t=0.5, t_before=0.5)

        if self.post:
            for post in self.post:
                self.run_sequence(post, data=experiment_data)
