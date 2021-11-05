from psychopy import core

from conflict_task.devices import DataHandler, InputDevice, Window
from conflict_task.sequence import Screen


class Instructions:
    def __init__(
        self, window: Window, input_device: InputDevice, instructions: list
    ) -> None:
        self.win = window
        self.input_device = input_device
        self.screens: list[Screen] = None

        if not isinstance(instructions, list):
            instructions = [instructions]
        for i, s in enumerate(instructions):
            if not isinstance(s, Screen):
                instructions[i] = Screen(s)

        self.screens = instructions

    def quit(self):
        self.win.flip()
        self.win.close()
        core.quit()

    def run_sequence(self, sequence: Screen):
        continue_experiment = sequence.run()

        DataHandler.add_data_dict_and_next_entry(sequence.get_data())

        if not continue_experiment:
            self.quit()

    def run(self):
        for screen in self.screens:
            self.run_sequence(screen)
