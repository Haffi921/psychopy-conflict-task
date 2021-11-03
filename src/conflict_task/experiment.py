from __future__ import annotations

from psychopy import clock, core, logging

from conflict_task.devices import DataHandler, Window, input_device
from conflict_task.devices.EMG_connector import EMGConnector
from conflict_task.util import get_type, get_type_or_fatal_exit, true_or_fatal_exit
from conflict_task.util.error import fatal_exit

from . import sequence


class Experiment:
    def __init__(
        self,
        experiment_settings: dict,
        trial_values: list = None,
        validate: bool = False,
    ) -> None:

        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------
        # Experiment settings
        self.name = None
        self.debug = None

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
        self.extra_info = None
        self.trial_values = (
            self.load_trial_values(trial_values, validate)
            if trial_values is not None
            else None
        )
        # -----------------------------------------------

        # -----------------------------------------------
        # Sanity check
        # -----------------------------------------------
        true_or_fatal_exit(
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

        self.debug = experiment_settings.get("debug", False)
        self.marker = get_type(experiment_settings, "marker", list, None)
        # -----------------------------------------------

        # -----------------------------------------------
        # Input device
        # -----------------------------------------------
        input_device_class = get_type(
            experiment_settings, "input_device", str, "Keyboard"
        )
        true_or_fatal_exit(
            hasattr(input_device, input_device_class),
            (
                "Input device specified in 'input_device' does not exist. "
                f"No input device named {input_device_class}"
            ),
        )
        self.input_device = getattr(input_device, input_device_class)()
        # -----------------------------------------------

        # -----------------------------------------------
        # Data handler
        # -----------------------------------------------
        if data_extra_info := experiment_settings.get("data_extra_info"):
            self.data_handler = DataHandler(
                experiment_name=self.name, subject_info=data_extra_info
            )
        else:
            self.data_handler = DataHandler(experiment_name=self.name)

        self.data_handler.start_participant_data()
        self.extra_info = {**self.data_handler.subject_info}
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
            "sequences",
            dict,
            "Experiment must have 'sequences' settings",
        )

        if pre_settings := get_type(experiment_sequence, "pre", list):
            for seq in pre_settings:
                self.pre.append(self._create_sequence(seq))

        if post_settings := get_type(experiment_sequence, "post", list):
            for seq in post_settings:
                self.post.append(self._create_sequence(seq))

        self.nr_blocks = get_type_or_fatal_exit(
            experiment_sequence, "nr_blocks", int, "'nr_blocks' must be specified"
        )
        self.nr_trials = get_type_or_fatal_exit(
            experiment_sequence, "nr_trials", int, "'nr_trials' must be specified"
        )

        self.nr_practice_blocks = get_type(experiment_sequence, "nr_practice_blocks", int, 0)
        self.nr_practice_trials = get_type(experiment_sequence, "nr_practice_trials", int, 0)

        if trial_settings := get_type_or_fatal_exit(
            experiment_sequence, "trial", dict, "'trial' settings must be specified"
        ):
            self.block_trial = self._create_sequence(trial_settings)

        if between_blocks_settings := get_type(experiment_sequence, "between_blocks", dict):
            self.between_blocks = self._create_sequence(between_blocks_settings)

        # if self.block_trial.takes_trial_values:
        #     true_or_fatal_exit(
        #         len(self.trial_values) == self.nr_blocks,
        #         (
        #             "Number of blocks in trial values not corresponding to 'nr_blocks': "
        #             f"{len(self.trial_values)} != {self.nr_blocks}"
        #         ),
        #     )
        #     true_or_fatal_exit(
        #         all(len(trials) == self.nr_trials for trials in self.trial_values),
        #         (
        #             "Number of trial values in all blocks must correspond to 'nr_trials': "
        #             f"{self.nr_trials}"
        #         ),
        #     )
        # -----------------------------------------------

    # ===============================================
    # Helper functions
    # ===============================================

    def _create_sequence(self, sequence_settings: dict) -> sequence.Sequence:
        if isinstance(sequence_settings, sequence.Sequence):
            return sequence_settings
        sequence_type = get_type(sequence_settings, "type", str, "Sequence")
        true_or_fatal_exit(
            hasattr(sequence, sequence_type),
            "Sequence type specified in 'type' does not exist. "
            f"No sequence named {sequence_type}",
        )
        return getattr(sequence, sequence_type)(
            self.window, self.input_device, sequence_settings
        )

    def _get_trial_values(self, block, trial) -> dict:
        if self.block_trial.takes_trial_values:
            return self.trial_values[block][trial]
        return {}

    def _get_all_sequences(self) -> list[sequence.Sequence]:
        return [*self.pre, self.block_trial, self.between_blocks, *self.post]

    def _get_all_trial_values(self) -> list[str]:
        requested_trial_values = []
        for seq in self._get_all_sequences():
            if seq.takes_trial_values:
                requested_trial_values.extend(seq._get_all_trial_values())
        return requested_trial_values

    def _abort(self):
        logging.warning("Aborting!")
        self.data_handler.abort()
        self.window.flip()
        self.window.close()
        core.quit()

    # ===============================================
    # Public member functions
    # ===============================================

    def validate_trial_values(self, trial_values) -> None:
        requested_trial_values = self._get_all_trial_values()
        nr_trial_values = len(requested_trial_values)
        if nr_trial_values:
            true_or_fatal_exit(
                len(trial_values) == self.nr_blocks + self.nr_practice_blocks,
                "Number of blocks of trial values does not match up with spcified block length "
                f"{len(trial_values)} (trial values) != {self.nr_blocks + self.nr_practice_blocks} (nr blocks)",
            )
            for block_nr, block_values in enumerate(trial_values):
                nr_trials = (
                    self.nr_practice_trials
                    if block_nr < self.nr_practice_blocks
                    else self.nr_trials
                )
                # TODO: Take in account practice
                true_or_fatal_exit(
                    len(block_values) == nr_trials,
                    "Number of trial values does not match up with spcified number of trials "
                    f"{len(block_values)} (trial values) != {nr_trials} (nr trials)"
                    f" in block nr {block_nr}",
                )
                for trial_nr, values in enumerate(block_values):
                    for key in requested_trial_values:
                        true_or_fatal_exit(
                            key in values,
                            "Trial values missing component request: "
                            f"Block {block_nr}, Trial {trial_nr} missing {key}",
                        )

    def load_trial_values(self, trial_values: list, validate: bool = False):

        # -----------------------------------------------
        # Sanity check
        # -----------------------------------------------
        true_or_fatal_exit(
            isinstance(trial_values, list)
            and all(isinstance(value, dict) for value in trial_values),
            "Trial values must be a list of dictionaries",
        )
        if self.block_trial.takes_trial_values:
            true_or_fatal_exit(
                len(self.trial_values) == self.nr_blocks,
                (
                    "Number of blocks in trial values not corresponding to 'nr_blocks': "
                    f"{len(self.trial_values)} != {self.nr_blocks}"
                ),
            )
            true_or_fatal_exit(
                all(len(trials) == self.nr_trials for trials in self.trial_values),
                (
                    "Number of trial values in all blocks must correspond to 'nr_trials': "
                    f"{self.nr_trials}"
                ),
            )
        # -----------------------------------------------

        self.trial_values = trial_values

        if validate:
            self.validate_trial_values(self.trial_values)

    def close(self):
        self.data_handler.finish_participant_data()
        self.window.flip()
        self.window.close()
        core.quit()

    def _run_sequence(self, seq: sequence.Sequence, trial_values={}):
        if seq is None:
            return

        continue_experiment = seq.run(trial_values, self.debug)

        self.data_handler.add_data_dict(self.extra_info)
        self.data_handler.add_data_dict(trial_values)
        self.data_handler.add_data_dict(seq.get_data())
        self.data_handler.next_entry()

        if not continue_experiment:
            if self.debug:
                self._abort()
            self.close()

    def _run_blocks(self, nr_blocks: int, nr_trials: int, practice=False):
        for block_nr in range(nr_blocks):
            block_info = {
                "trial_block": "practice" if practice else "block",
                "block": block_nr + 1,
            }
            trial_values = self.trial_values[
                block_nr + (self.nr_practice_blocks if not practice else 0)
            ]
            if block_nr:
                self._run_sequence(self.between_blocks)

            if self.marker:
                marker_start = (
                    self.marker[0]
                    + block_nr
                    + (self.nr_practice_blocks if not practice else 0)
                )
                EMGConnector.send_marker(marker_start, t=0.5, t_after=0.5)

            for trial_nr in range(nr_trials):
                trial_values = {
                    **block_info,
                    "trial": trial_nr + 1,
                    **trial_values[trial_nr],
                }
                self._run_sequence(self.block_trial, trial_values)

            if self.marker:
                marker_start = (
                    self.marker[1]
                    + block_nr
                    + (self.nr_practice_blocks if not practice else 0)
                )
                EMGConnector.send_marker(marker_start, t=0.5, t_before=0.5)

    def run(self):    
        for pre in self.pre:
            self._run_sequence(pre)

        self._run_blocks(
            nr_blocks=self.nr_practice_blocks,
            nr_trials=self.nr_practice_trials,
            practice=True,
        )

        self._run_sequence(self.between_blocks)

        self._run_blocks(
            nr_blocks=self.nr_blocks,
            nr_trials=self.nr_trials,
        )

        for post in self.post:
            self._run_sequence(post)

        self.close()
