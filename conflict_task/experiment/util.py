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