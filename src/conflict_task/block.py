from __future__ import annotations

from psychopy import clock, core, logging

from conflict_task.devices import DataHandler, Window, InputDevice
from conflict_task.devices.EMG_connector import EMGConnector
from conflict_task.sequence import Sequence, Screen, Trial
from conflict_task.util import get_or_fatal_exit, get_type, get_type_or_fatal_exit, true_or_fatal_exit


class Block:
    def __init__(self, win: Window, input_device: InputDevice, block_settings: dict = {}) -> None:
        self.win = win
        self.input_device = input_device

        self.marker: list = None

        self.trial: Trial = None
        self.between_screen: Screen = None
        self.post_screen: Screen = None
        
        self._parse_block_settings(block_settings)
    
    def _parse_block_settings(self, block_settings: dict):
        self.marker = get_type(block_settings, "marker", list)
        self._parse_sequence_settings(block_settings)

    def _parse_sequence_settings(self, block_settings: dict):
        self.trial = get_or_fatal_exit(block_settings, "trial", "Block settings must have 'trial' settings")
        if not isinstance(self.trial, Trial):
            self.trial = Trial(self.win, self.input_device, self.trial)
        
        self.between_screen = block_settings.get("between")
        if not isinstance(self.between_screen, Screen):
            self.between_screen = Screen(self.win, self.input_device, self.between_screen)
        
        self.post_screen = block_settings.get("post")
        if not isinstance(self.post_screen, Trial):
            self.post_screen = Screen(self.win, self.input_device, self.post_screen)

    def quit(self):
        self.win.flip()
        self.win.close()
        core.quit()

    def run_sequence(self, sequence: Sequence, trial_values = {}, data = {}):
        continue_experiment = sequence.run(trial_values)

        DataHandler.add_data_dict_and_next_entry(
            {**data, **sequence.get_data()}
        )

        if not continue_experiment:
            self.quit()

    def run(self, nr_blocks: int, nr_trial: int, trial_values_list: list[list[dict]] = [], experiment_data: dict = {}):
        for block in range(nr_blocks):
            block_data = {
                **experiment_data,
                "block": block + 1,
            }
            if self.between_screen and block:
                self.run_sequence(self.between_screen, data = block_data)

            if self.marker:
                EMGConnector.send_marker(self.marker[0] + block, t=0.5, t_after=0.5)

            for trial in range(1, nr_trial + 1):
                trial_values = {**block_data, "trial": trial, **trial_values_list[block][trial]}

                self.run_sequence(self.trial, trial_values = trial_values, data = trial_values)
            
            if self.marker:
                EMGConnector.send_marker(self.marker[1] + block, t=0.5, t_before=0.5)
        
        if self.post_screen:
            self.run_sequence(self.post_screen, data = experiment_data)()
