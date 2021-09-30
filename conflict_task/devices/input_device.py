from psychopy import logging, core

from psychopy.hardware import keyboard

from conflict_task.util import *

class InputDevice:


    def __init__(self):
        self.device = None


    def _use_derived_classes():
        fatal_exit("InputDevice: Use derived classes")
    

    def get_keys(self, keys: list[str]) -> list[tuple[str, float]]:
        """
        Derived classes need to implement this on for their own devices
        """      

        self._use_derived_classes()
    

    def get_last_key(self, keys: list[str]) -> tuple[str, float]:
        self._use_derived_classes()
    

    def was_key_pressed(self, keys) -> bool:
        self._use_derived_classes()
    

    def reset_clock(self, newT=0.0):
        self._use_derived_classes()


class Keyboard(InputDevice):


    def __init__(self):
        self.device = keyboard.Keyboard()
    

    def get_keys(self, keys: list[str]) -> list[tuple[str, float]]:
        if isinstance(keys, str):
            keys = [keys]
        
        return [(key.name, key.rt) for key in self.device.getKeys(keys)]
    

    def get_last_key(self, keys: list[str]) -> tuple[str, float]:
        keys_pressed = self.get_keys(keys)

        if len(keys_pressed):
            return keys_pressed[-1]
        else:
            return None
    

    def was_key_pressed(self, keys) -> bool:
        key_pressed = self.get_keys(keys)

        if len(key_pressed):
            return True
        else:
            return False
    

    def reset_clock(self, newT = 0.0):
        self.device.clock.reset(newT)