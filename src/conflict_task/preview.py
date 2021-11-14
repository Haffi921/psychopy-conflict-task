from conflict_task import sequence
from conflict_task.component import (
    AudioComponent,
    BaseComponent,
    ResponseComponent,
    VisualComponent,
    WaitComponent,
)
from conflict_task.constants import *
from conflict_task.devices import InputDevice, Window


def preview_component(
    component_settings, component_values={}, window_settings={}, component_type=VISUAL
):
    Window.start(window_settings)
    component: BaseComponent = None

    if component_type is VISUAL:
        component = VisualComponent(component_settings)
    elif component_type is AUDIO:
        component = AudioComponent(component_settings)
    elif component_type is RESPONSE:
        component = ResponseComponent(component_settings)
    elif component_type is WAIT:
        component = WaitComponent(component_settings)

    if component.variable_factor:
        component.prepare(component_values)

    print(component.component.size)

    running = KEEP_RUNNING

    component.start(0, 0, 0)

    while running == KEEP_RUNNING:
        if InputDevice.was_key_pressed("escape"):
            running = QUIT_EXPERIMENT
            continue

        if component_type == RESPONSE:
            component.check()

            if component.made:
                running = STOP_RUNNING

        Window.flip()


def preview_sequence(sequence_settings, sequence_values={}, window_settings={}, print_data = False):
    if not Window.started:
        Window.start(window_settings)
    InputDevice()

    if "type" in sequence_settings and hasattr(sequence, sequence_settings["type"]):
        seq = getattr(sequence, sequence_settings["type"])(sequence_settings)
    else:
        seq = sequence.Sequence(sequence_settings)
    
    seq.run(sequence_values, False)
    
    if print_data:
        for data, value in seq.get_data().items():
            print(data, value)
