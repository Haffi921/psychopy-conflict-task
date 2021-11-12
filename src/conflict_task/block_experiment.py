from conflict_task.block import Block
from conflict_task.devices import DataHandler, EMGConnector, Window
from conflict_task.instructions import Instructions
from conflict_task.util.dictionary import get_type_or_fatal_exit


class BlockExperiment:
    def __init__(self, experiment_settings: dict) -> None:
        self.name = None

        self.instructions: Instructions = None

        self.practice_block: Block = None
        self.nr_practice_blocks: int = 0
        self.nr_practice_trials: int = None

        self.trial_block: Block = None
        self.nr_blocks: int = 0
        self.nr_trials: int = None

        self._parse_experiment_settings(experiment_settings)

    def _parse_experiment_settings(self, experiment_settings: dict):
        self.name = get_type_or_fatal_exit(
            experiment_settings, "name", str, "Please specify experiment 'name'"
        )
        dlg_info = experiment_settings.get("extra_info", {})

        DataHandler.start_participant_data(self.name, dlg_info=dlg_info)

        if experiment_settings.get("marker", False):
            EMGConnector.connect()

        Window.start()

        self.instructions = experiment_settings.get("instructions")
        if not isinstance(self.instructions, Instructions):
            self.instructions = Instructions(self.instructions)

        block_settings: dict = get_type_or_fatal_exit(
            experiment_settings,
            "blocks",
            dict,
            "Experiment settings must include key 'block' - none found",
        )

        if practice := block_settings.get("practice_block"):
            self.practice_block = Block(practice)

        self.trial_block = Block(block_settings.get("trial_block"))

    def get_participant_number(self):
        return DataHandler.get_participant_number()

    def quit(self):
        DataHandler.finish_participant_data()
        Window.quit()

    def run(self, practice_trial_values: list = [], trial_values: list = []):
        if self.instructions:
            self.instructions.run()

        if self.practice_block:
            self.practice_block.run(practice_trial_values, {"trial_block": "practice"})

        self.trial_block.run(trial_values, {"trial_block": "trial"})

        self.quit()
