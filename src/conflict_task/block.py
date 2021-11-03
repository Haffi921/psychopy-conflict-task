from __future__ import annotations

from psychopy import clock, core, logging

from conflict_task.devices import DataHandler, Window, InputDevice
from conflict_task.devices.EMG_connector import EMGConnector
from conflict_task.sequence import Sequence, Screen, Trial
from conflict_task.util import get_type, get_type_or_fatal_exit, true_or_fatal_exit
from conflict_task.util.error import fatal_exit


class Block:
    def __init__(self, win: Window, input_device: InputDevice, data_handler: DataHandler, trial: Trial, between_screen: Screen = None, post_screen: Screen = None, block_settings: dict = {}) -> None:
        self.win = win
        self.input_device = input_device
        self.data_handler = data_handler

        self.trial: Trial = None
        self.between_screen: Screen = None
        self.post_screen: Screen = None

        self.marker: list = None

        # Parse
        self.trial = trial
        self.between_screen = between_screen
        self.post_screen = post_screen
        
        #self._parse_block_settings(block_settings)
        #self._parse_sequence_settings(win, block_settings)
    
    # def _parse_sequence_settings(self, win: Window, input_device: InputDevice, block_settings: dict):
    #     self.trial = Trial(win, input_device, block_settings)

    def quit(self):
        self.data_handler.finish_participant_data()
        self.win.flip()
        self.win.close()
        core.quit()

    def run_sequence(self, sequence: Sequence, trial_values = {}, data = {}):
        continue_experiment = sequence.run(trial_values)

        self.data_handler.add_data_dict_and_next_entry(
            {**data, **sequence.get_data()}
        )

        if not continue_experiment:
            self.quit()

    def run(self, nr_blocks: int, nr_trial: int, trial_values_list: list[list[dict]] = [], experiment_data: dict = {}):
        for block in range(1, nr_blocks + 1):
            block_data = {
                **experiment_data,
                "block": block,
            }
            if self.marker:
                    EMGConnector.send_marker(self.marker[0] + block, t=0.5, t_after=0.5)

            for trial in range(1, nr_trial + 1):
                trial_values = {**block_data, "trial": trial, **trial_values_list[block][trial]}

                self.run_sequence(self.trial, trial_values = trial_values, data = trial_values)
            
            if self.marker:
                EMGConnector.send_marker(self.marker[1] + block, t=0.5, t_before=0.5)
            
            if self.between_screen:
                self.run_sequence(self.between_screen, data = block_data)
        
        if self.post_screen:
            self.run_sequence(self.post_screen, data = experiment_data)()