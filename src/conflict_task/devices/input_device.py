from __future__ import annotations

from psychopy.hardware import keyboard

from conflict_task.util import *


class InputDevice:
    def __init__(self):
        self.device = None

    def _use_derived_classes(self):
        true_or_fatal_exit(
            self.__class__.__name__ != "InputDevice",
            "InputDevice: Use derived classes",
        )

    def get_keys(self, keys: list[str]) -> list[tuple[str, float]]:
        """
        Derived classes need to implement this on for their own devices
        """

        self._use_derived_classes()

    def get_last_key(self, keys: list[str]) -> tuple[str, float]:
        self._use_derived_classes()

    def was_key_pressed(self, keys) -> bool:
        self._use_derived_classes()

    def reset_clock(self, new_t=0.0):
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
        return None

    def was_key_pressed(self, keys) -> bool:
        key_pressed = self.get_keys(keys)

        return bool(len(key_pressed))

    def reset_clock(self, new_t=0.0):
        self.device.clock.reset(new_t)

    def reset_events(self):
        self.device.clearEvents()
