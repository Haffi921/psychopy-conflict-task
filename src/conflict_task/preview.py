from conflict_task import sequence
from conflict_task.component import *
from conflict_task.constants import *
from conflict_task.devices import Keyboard, Window


def preview_component(
    component_settings, component_type=VISUAL, component_values={}, window_settings={}
):
    window = Window(window_settings)
    keyboard = Keyboard()
    component: BaseComponent = None

    if component_type == VISUAL:
        component = VisualComponent(component_settings, window)
    elif component_type == AUDIO:
        component = AudioComponent(component_settings)
    elif component_type == RESPONSE:
        component = ResponseComponent(component_settings)
    elif component_type == WAIT:
        component = WaitComponent(component_settings)

    if component.variable_factor:
        component.prepare(component_values)

    running = KEEP_RUNNING

    component.start(0, 0, 0)

    while running == KEEP_RUNNING:
        if keyboard.was_key_pressed("escape"):
            running = QUIT_EXPERIMENT
            continue

        if component_type == RESPONSE:
            component.check(keyboard)

            if component.made:
                running = STOP_RUNNING

        window.flip()


def preview_sequence(sequence_settings, sequence_values={}, window_settings={}):
    window = Window(window_settings)
    keyboard = Keyboard()

    if "type" in sequence_settings and hasattr(sequence, sequence_settings["type"]):
        seq = getattr(sequence, sequence_settings["type"])(
            window, keyboard, None, sequence_settings
        )
    else:
        seq = sequence.Sequence(window, keyboard, None, sequence_settings)

    seq.run(sequence_values, False)
