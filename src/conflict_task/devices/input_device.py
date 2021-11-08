from __future__ import annotations

from psychopy.hardware import keyboard

from conflict_task.util import *


class InputDeviceBase:
    _device = None

    @classmethod
    def _use_derived_classes(cls):
        true_or_fatal_exit(
            cls.__class__.__name__ != "InputDevice",
            "InputDevice: Use derived classes",
        )

    @classmethod
    def get_keys(
        cls, keys: list[str], wait_for_release=False
    ) -> list[tuple[str, float]]:
        cls._use_derived_classes()

    @classmethod
    def get_last_key(cls, keys: list[str]) -> tuple[str, float]:
        cls._use_derived_classes()

    @classmethod
    def was_key_pressed(cls, keys) -> bool:
        cls._use_derived_classes()

    @classmethod
    def reset_clock(cls, new_t=0.0) -> None:
        cls._use_derived_classes()

    @classmethod
    def reset_events(cls) -> None:
        cls._use_derived_classes()


"""
class Keyboard(InputDevice):
    def __init__(self):
        self.device = keyboard.Keyboard()

    def get_keys(
        self, keys: list[str], wait_for_release=False, clear=True
    ) -> list[tuple[str, float]]:
        if isinstance(keys, str):
            keys = [keys]

        return [
            (key.name, key.rt)
            for key in self.device.getKeys(
                keys, waitRelease=wait_for_release, clear=clear
            )
        ]

    def get_last_key(self, keys: list[str]) -> tuple[str, float]:
        keys_pressed = self.get_keys(keys)

        if len(keys_pressed):
            return keys_pressed[-1]
        return None

    def was_key_pressed(self, keys, clear=False) -> bool:
        key_pressed = self.get_keys(keys, clear=clear)

        return bool(len(key_pressed))

    def reset_clock(self, new_t=0.0):
        self.device.clock.reset(new_t)

    def reset_events(self):
        self.device.clearEvents()
"""


class Keyboard(InputDeviceBase):
    _device = keyboard.Keyboard()

    @classmethod
    def get_keys(
        cls, keys: list[str], wait_for_release=False, clear=True
    ) -> list[tuple[str, float]]:
        if isinstance(keys, str):
            keys = [keys]

        return [
            (key.name, key.rt)
            for key in cls._device.getKeys(
                keys, waitRelease=wait_for_release, clear=clear
            )
        ]

    @classmethod
    def get_last_key(cls, keys: list[str]) -> tuple[str, float]:
        keys_pressed = cls.get_keys(keys)

        if len(keys_pressed):
            return keys_pressed[-1]
        return None

    @classmethod
    def was_key_pressed(cls, keys, clear=False) -> bool:
        key_pressed = cls.get_keys(keys, clear=clear)

        return bool(len(key_pressed))

    @classmethod
    def reset_clock(cls, new_t=0.0) -> None:
        cls._device.clock.reset(new_t)

    @classmethod
    def reset_events(cls) -> None:
        cls._device.clearEvents()


INPUT_DEVICES = {"Keyboard": Keyboard}


class InputDevice:
    instance = Keyboard

    @classmethod
    def select(cls, input_device: InputDeviceBase):
        try:
            if isinstance(input_device, str):
                input_device = INPUT_DEVICES[input_device]
            if isinstance(input_device, InputDeviceBase):
                cls.instance = input_device
            else:
                raise ValueError
        except (KeyError, ValueError):
            fatal_exit(
                f"{input_device} is not a valid input device. "
                "Please select any of the following {INPUT_DEVICES}"
            )

    @classmethod
    def get_keys(
        cls, keys: list[str], wait_for_release=False, clear=True
    ) -> list[tuple[str, float]]:
        return cls.instance.get_keys(keys, wait_for_release, clear)

    @classmethod
    def get_last_key(cls, keys: list[str]) -> tuple[str, float]:
        return cls.instance.get_last_key(keys)

    @classmethod
    def was_key_pressed(cls, keys, clear=False) -> bool:
        return cls.instance.was_key_pressed(keys, clear)

    @classmethod
    def reset_clock(cls, new_t=0.0) -> None:
        cls.reset_clock(new_t)

    @classmethod
    def reset_events(cls) -> None:
        cls.reset_events
