from psychopy import core, clock, logging

from conflict_task.devices import data_handler, input_device
from conflict_task.devices import Window, DataHandler

from . import sequence

class Experiment:

    def __init__(self, name, trial_values, experiment_settings: dict):
        
        self.name = name
        self.trial_values = trial_values
        self.clock = clock.Clock()
        self.allow_escape = experiment_settings.get("allow_escape", False)


        # Data handler
        if "subjectInfo" in experiment_settings:
            self.data_handler = DataHandler(self.name, experiment_settings["subjectInfo"])
        else:
            self.data_handler = DataHandler(self.name)
        

        # Input device
        if "input_device" in experiment_settings:
            if hasattr(input_device, experiment_settings["input_device"]):
                self.input_device = getattr(input_device, experiment_settings["input_device"])
            else:
                logging.fatal(f"No input device named {experiment_settings['input_device']}")
                core.quit()
        else:
            self.input_device = input_device.Keyboard()
        

        # Debug data
        if "debug_data" in experiment_settings:
            self.debug_data = bool(experiment_settings["debug_data"])
        

        # Window
        if "window_settings" in experiment_settings:
            self.window = Window(experiment_settings["window_settings"])
        else:
            self.window = Window()

        
        # Sequences        
        if "experiment_sequence" in experiment_settings:
            if "pre" in experiment_settings["experiment_sequence"]:
                self.pre: list[sequence.Sequence] = []
                for seq in experiment_settings["experiment_sequence"]["pre"]:
                    self.pre.append(self.create_sequence(seq))
            
            if "post" in experiment_settings["experiment_sequence"]:
                self.post: list[sequence.Sequence] = []
                for seq in experiment_settings["experiment_sequence"]["post"]:
                    self.post.append(self.create_sequence(seq))
            
            if "block" in experiment_settings["experiment_sequence"]:
                self.nr_blocks = experiment_settings["experiment_sequence"]["nr_blocks"]
                self.nr_trials = experiment_settings["experiment_sequence"]["nr_trials"]
                self.block_trial: sequence.Sequence = self.create_sequence(experiment_settings["experiment_sequence"]["trial"])
                self.between_block: sequence.Sequence = self.create_sequence(experiment_settings["experiment_sequence"]["between_blocks_screen"])


    def create_sequence(self, sequence_settings: dict) -> sequence.Sequence:
        if "type" in sequence_settings:
            return getattr(sequence, sequence_settings["type"])(
                self.window, self.input_device, self.data_handler, sequence_settings
                )
        else:
            return sequence.Sequence(self.window, self.input_device, self.data_handler, sequence_settings)
    

    def close(self):
        self.data_handler.finish_participant_data()
        self.window.flip()
        self.window.close()
        core.quit()


    def run(self, debug_data = False):
        continue_experiment = True


        # PRE
        for pre in self.pre:
            continue_experiment = pre.run(debug_data=debug_data, allow_escape=self.allow_escape)

            if not continue_experiment:
                self.close()


        # BLOCK
        for block in range(self.nr_blocks):
            for trial in range(self.nr_trials):
                trial_values = {}
                if self.block_trial.takes_trial_values:
                    trial_values = trial_values | self.trial_values[block][trial]

                self.data_handler.add_data_dict(trial_values)

                continue_experiment = self.block_trial.run(trial_values=trial_values, allow_escape=self.allow_escape)

                self.data_handler.next_entry()

                if not continue_experiment:
                    self.close()

            # BETWEEN BLOCK
            if block < self.nr_blocks - 1:            
                continue_experiment = self.between_block.run(allow_escape=self.allow_escape)

                if not continue_experiment:
                    self.close()
        

        # POST
        for post in self.post:
            continue_experiment = post.run(debug_data=debug_data, allow_escape=self.allow_escape)

            if not continue_experiment:
                self.close()
        
        self.close()