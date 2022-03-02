from conflict_task.devices import DataHandler, Window
from conflict_task.devices.window import Window
from conflict_task.sequence import Screen
from conflict_task.util.dictionary import (
    get_or_fatal_exit,
    get_type,
    get_type_or_fatal_exit,
)


class Instructions:
    def __init__(self, instruction_settings: dict) -> None:
        self.pages: list[Screen] = None
        self._index: int = 0

        self.key_forward: str = None
        self.allow_backward: bool = True
        self.key_backward: str = None

        self._parse_instruction_settings(instruction_settings)

    def _parse_instruction_settings(self, instruction_settings):
        self.key_forward = get_type_or_fatal_exit(
            instruction_settings, "key_forward", str, "Please indicate forward key"
        )

        self.allow_backward = get_type(
            instruction_settings, "allow_backward", bool, True
        )

        if self.allow_backward:
            self.key_backward = get_type_or_fatal_exit(
                instruction_settings,
                "key_backward",
                str,
                "Please indicate backward key",
            )

        instructions = get_or_fatal_exit(
            instruction_settings,
            "screens",
            "Please include some screens in instructions",
        )

        response = {"response": {"keys": [self.key_forward]}}

        if self.allow_backward:
            response["response"]["keys"].append(self.key_backward)

        if not isinstance(instructions, list):
            instructions = [instructions]
        for i, s in enumerate(instructions):
            if not isinstance(s, Screen):
                instructions[i] = Screen({**s, **response})

        self.pages = instructions

    def run_sequence(self, sequence: Screen):
        continue_experiment = sequence.run()

        DataHandler.add_data_dict_and_next_entry(sequence.get_data())

        if not continue_experiment:
            Window.quit()

    def get_current_page(self):
        return self.pages[self._index]

    def go_forward(self):
        self._index = min(self._index + 1, len(self.pages))

    def go_backward(self):
        if self.allow_backward:
            self._index = max(0, self._index - 1)

    def run(self):
        while self._index < len(self.pages):
            page = self.get_current_page()

            self.run_sequence(page)

            if page.response.made:
                if page.response.key == self.key_forward:
                    self.go_forward()
                elif self.allow_backward and page.response.key == self.key_backward:
                    self.go_backward()
