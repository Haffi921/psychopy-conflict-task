from psychopy import clock, core

from conflict_task.devices import DataHandler, Window, input_device
from conflict_task.util import *

from . import sequence


class Experiment:
    def __init__(self, trial_values: list, experiment_settings: dict) -> None:

        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------
        # Experiment settings
        self.name = None
        self.allow_escape = None

        # Devices
        self.input_device: input_device.InputDevice = None
        self.data_handler: DataHandler = None
        self.window: Window = None
        self.clock = clock.Clock()

        # Sequences
        self.pre: list[sequence.Sequence] = []
        self.post: list[sequence.Sequence] = []
        self.block_trial: sequence.Sequence = None
        self.between_blocks: sequence.Sequence = None

        # Values
        self.trial_values = trial_values
        # -----------------------------------------------

        # -----------------------------------------------
        # Sanity check
        # -----------------------------------------------
        test_or_fatal_exit(
            isinstance(trial_values, list),
            "Trial values must be a list of dictionaries",
        )
        test_or_fatal_exit(
            isinstance(experiment_settings, dict),
            "Experiment settings must be a dictionary",
        )
        # -----------------------------------------------

        # -----------------------------------------------
        # Parse settings
        self._parse_experiment_settings(experiment_settings)
        # -----------------------------------------------

    # ===============================================
    # Dictionary parsing
    # ===============================================
    def _parse_experiment_settings(self, experiment_settings: dict) -> None:

        # -----------------------------------------------
        # Experiment settings
        # -----------------------------------------------
        self.name = get_type_or_fatal_exit(
            experiment_settings, "name", str, "Please specify experiment 'name'"
        )
        self.allow_escape = experiment_settings.get("allow_escape", False)
        # -----------------------------------------------

        # -----------------------------------------------
        # Input device
        # -----------------------------------------------
        input_device_class = get_type(
            experiment_settings, "input_device", str, "Keyboard"
        )
        test_or_fatal_exit(
            hasattr(input_device, input_device_class),
            f"Input device specified in 'input_device' does not exist. No input device named {input_device_class}",
        )
        self.input_device = getattr(input_device, input_device_class)
        # -----------------------------------------------

        # -----------------------------------------------
        # Data handler
        # -----------------------------------------------
        if subjectInfo := experiment_settings.get("subjectInfo"):
            self.data_handler = DataHandler(self.name, subjectInfo=subjectInfo)
        else:
            self.data_handler = DataHandler(self.name)
        # -----------------------------------------------

        # -----------------------------------------------
        # Window
        # -----------------------------------------------
        if window_settings := experiment_settings.get("window_settings"):
            self.window = Window(window_settings)
        else:
            self.window = Window()
        # -----------------------------------------------

        # -----------------------------------------------
        # Sequences
        # -----------------------------------------------
        experiment_sequence: dict = get_type_or_fatal_exit(
            experiment_settings,
            "experiment_sequence",
            dict,
            "Experiment must have 'sequence' settings",
        )

        if pre_settings := get_type(experiment_settings, "pre", list):
            for seq in pre_settings:
                self.pre.append(self._create_sequence(seq))

        if post_settings := get_type(experiment_sequence, "post", list):
            for seq in post_settings:
                self.post.append(self._create_sequence(seq))

        block_settings: dict = get_type_or_fatal_exit(
            experiment_sequence,
            "block",
            dict,
            "Experiment sequence must have 'block' settings",
        )

        self.nr_blocks = get_type_or_fatal_exit(
            block_settings, "nr_blocks", int, "'nr_blocks' must be specified"
        )
        self.nr_trials = get_type_or_fatal_exit(
            block_settings, "nr_trials", int, "'nr_trials' must be specified"
        )

        if trial_settings := get_type_or_fatal_exit(
            block_settings, "trial", dict, "'trial' settings must be specified"
        ):
            self.block_trial = self._create_sequence(trial_settings)

        if between_blocks_settings := get_type(block_settings, "between_blocks", dict):
            self.between_blocks = self._create_sequence(between_blocks_settings)

        if self.block_trial.takes_trial_values:
            test_or_fatal_exit(
                len(self.trial_values) == self.nr_blocks,
                f"Number of blocks in trial values not corresponding to 'nr_blocks' - {len(self.trial_values)} != {self.nr_blocks}",
            )
            test_or_fatal_exit(
                all(len(trials) == self.nr_trials for trials in self.trial_values),
                f"Number of trial values in all blocks must correspond to 'nr_trials' = {self.nr_trials}",
            )
        # -----------------------------------------------

    # ===============================================
    # Helper functions
    # ===============================================

    def _create_sequence(self, sequence_settings: dict) -> sequence.Sequence:
        sequence_type = get_type(sequence_settings, "type", str, "Sequence")
        test_or_fatal_exit(
            isinstance(sequence, sequence_type),
            f"Sequence type specified in 'type' does not exist. No sequence named {sequence_type}",
        )
        return getattr(sequence, sequence_type)(
            self.window, self.input_device, sequence_settings
        )

    def _get_trial_values(self, block, trial) -> dict:
        if self.block_trial.takes_trial_values:
            return self.trial_values[block][trial]
        else:
            return {}

    # ===============================================
    # Public member functions
    # ===============================================

    def close(self):
        self.data_handler.finish_participant_data()
        self.window.flip()
        self.window.close()
        core.quit()

    def run(self, debug_data=False):
        continue_experiment = True

        self.data_handler.start_participant_data()

        experiment_data = {"experiment_name": self.name}

        # PRE
        for pre in self.pre:
            continue_experiment = pre.run(allow_escape=self.allow_escape)

            self.data_handler.add_data_dict_and_next_entry(
                experiment_data | pre.get_data()
            )

            if not continue_experiment:
                self.close()

        for block in range(self.nr_blocks):
            block_data = experiment_data | {"block": block + 1}

            # BETWEEN BLOCK
            if block:  # Skip first block
                continue_experiment = self.between_blocks.run(
                    allow_escape=self.allow_escape
                )

                self.data_handler.add_data_dict_and_next_entry(
                    block_data | self.between_blocks.get_data()
                )

                if not continue_experiment:
                    self.close()

            # BLOCK
            for trial in range(self.nr_trials):
                trial_data = block_data | {"trial": trial + 1}

                trial_values = trial_data | self._get_trial_values(block, trial)

                continue_experiment = self.block_trial.run(
                    trial_values=trial_values, allow_escape=self.allow_escape
                )

                self.data_handler.add_data_dict(trial_values)
                self.data_handler.add_data_dict_and_next_entry(
                    self.block_trial.get_data()
                )

                if not continue_experiment:
                    self.close()

        # POST
        for post in self.post:
            continue_experiment = post.run(
                debug_data=debug_data, allow_escape=self.allow_escape
            )

            if not continue_experiment:
                self.close()

        self.close()
