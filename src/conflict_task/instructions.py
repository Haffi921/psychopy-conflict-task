from conflict_task.devices import DataHandler, Window
from conflict_task.devices.window import Window
from conflict_task.sequence import Screen


class Instructions:
    def __init__(self, instructions: list) -> None:
        self.screens: list[Screen] = None

        if not isinstance(instructions, list):
            instructions = [instructions]
        for i, s in enumerate(instructions):
            if not isinstance(s, Screen):
                instructions[i] = Screen(s)

        self.screens = instructions

    def run_sequence(self, sequence: Screen):
        continue_experiment = sequence.run()

        DataHandler.add_data_dict_and_next_entry(sequence.get_data())

        if not continue_experiment:
            Window.quit()

    def run(self):
        for screen in self.screens:
            self.run_sequence(screen)
