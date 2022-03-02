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
    if not Window.started:
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

    if component.variable_factor is not None:
        component.prepare(component_values)

    print(component.component.size)

    running = KEEP_RUNNING

    component.start(0, 0, 0)

    while running == KEEP_RUNNING:
        if InputDevice.was_key_pressed("escape"):
            running = QUIT_EXPERIMENT
            continue
        elif InputDevice.was_key_pressed("space", clear=True):
            running = STOP_RUNNING

        if component_type == RESPONSE:
            component.check()

            if component.made:
                running = STOP_RUNNING

        Window.flip()

    component.stop(0, 0, 0)


def preview_sequence(
    sequence_settings, sequence_values={}, window_settings={}, print_data=False
):
    if not Window.started:
        Window.start(window_settings)

    if "type" in sequence_settings and hasattr(sequence, sequence_settings["type"]):
        seq = getattr(sequence, sequence_settings["type"])(sequence_settings)
    else:
        seq = sequence.Sequence(sequence_settings)

    seq.start_persistent()

    if isinstance(sequence_values, list):
        for value in sequence_values:
            success = seq.run(value, True)
            if not success:
                break
    else:
        success = seq.run(sequence_values, True)

    seq.stop_persistent()

    if print_data:
        for data, value in seq.get_data().items():
            print(data, value)

    if success == QUIT_EXPERIMENT:
        Window.quit()

    seq._stop_all_components(0, 0, 0)
    InputDevice.reset_events()
    Window.turnoff()
