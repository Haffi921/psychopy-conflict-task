from psychopy.hardware import keyboard

class InputDevice:
    device = None

    def __init__(self, deviceClass):
        self.device = deviceClass()

class Keyboard(InputDevice):
    def __init__(self):
        super().__init__(keyboard.Keyboard)