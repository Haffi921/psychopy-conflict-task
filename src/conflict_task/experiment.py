from __future__ import annotations

from psychopy import clock

from conflict_task.block_experiment import BlockExperiment
from conflict_task.devices.EMG_connector import EMGConnector
from conflict_task.instructions import Instructions
from conflict_task.util import get_type_or_fatal_exit


class Experiment:
    def __init__(self, experiment_settings: dict) -> None:

        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------
        # Experiment settings
        self.name = None

        self.clock = clock.Clock()

        # Sequences
        self.instructions: Instructions = None
        self.block_experiment: BlockExperiment = None

        # Values
        self.extra_info = None
        # -----------------------------------------------

        # -----------------------------------------------
        # Parse settings
        # -----------------------------------------------
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
        # -----------------------------------------------

        # -----------------------------------------------
        # Sequences
        # -----------------------------------------------
        self.instructions = Instructions(experiment_settings.get("instructions"))
        self.block_experiment = BlockExperiment(experiment_settings.get("blocks"))
        # -----------------------------------------------

    """
    # ===============================================
    # Helper functions
    # ===============================================

    def _get_all_trial_values(self) -> list[str]:
        requested_trial_values = []
        for seq in self._get_all_sequences():
            if seq.takes_trial_values:
                requested_trial_values.extend(seq._get_all_trial_values())
        return requested_trial_values

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
    """

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
