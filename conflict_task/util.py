from psychopy import logging, core

from conflict_task.constants import *
from conflict_task.devices import Window, Keyboard

from .component import *
from . import sequence

def preview_component(component_settings, type = VISUAL, component_values = {}, window_settings = {}):
    window = Window(window_settings)
    keyboard = Keyboard()
    component: BaseComponent = None

    if type == VISUAL:
        component = VisualComponent(component_settings, window)
    elif type == AUDIO:
        component = AudioComponent(component_settings)
    elif type == RESPONSE:
        component = ResponseComponent(component_settings)
    elif type == WAIT:
        component = WaitComponent(component_settings)

    if component.variable_factor:
        component.prepare(component_values)
    
    running = KEEP_RUNNING

    component.start(0, 0, 0)

    while running == KEEP_RUNNING:
        if keyboard.was_key_pressed("escape"):
            running = QUIT_EXPERIMENT
            continue

        if type == RESPONSE:
            component.check(keyboard)

            if component.made:
                running = STOP_RUNNING
            
        window.flip()


def preview_sequence(sequence_settings, sequence_values = {}, window_settings = {}):
    window = Window(window_settings)
    keyboard = Keyboard()

    if "type" in sequence_settings and hasattr(sequence, sequence_settings["type"]):
        seq = getattr(sequence, sequence_settings["type"])(window, keyboard, None, sequence_settings)
    else:
        seq = sequence.Sequence(window, keyboard, None, sequence_settings)

    seq.run(sequence_values, False)


def fatal_exit(msg: str):
    logging.fatal(msg)
    core.quit()


def test_or_fatal_exit(test: bool, msg: str):
    if not test:
        fatal_exit(msg)


def get_or_fatal_exit(dictionary: dict, key: str, msg: str):
    if value := dictionary.get(key):
        return value
    else:
        fatal_exit(msg)


def get_type_or_fatal_exit(dictionary: dict, key: str, type_name: object, msg: str):
    value = get_or_fatal_exit(dictionary, key, msg)

    if not isinstance(value, type_name):
        fatal_exit(f"'{key}' must be of type '{type_name}'")
    
    return value


def get_type(dictionary: dict, key: str, type_name: object, *args, **kwargs):
    if value := dictionary.get(key, *args, **kwargs):
        if not isinstance(value, type_name):
            fatal_exit(f"'{key}' must be of type '{type_name}'")

    return value