from psychopy import clock
from psychopy.data import ExperimentHandler

from conflict_task.devices import Window, InputDevice, input_device

from ..component import *


FRAMETOLERANCE = 0.001


class BaseSequence:
    window: Window
    input_device: InputDevice
    data_handler: ExperimentHandler

    response: ResponseComponent
    visual: list[VisualComponent]
    audio: list[AudioComponent]
    wait: list[WaitComponent]

    clock = clock.Clock()

    wait_for_response: bool = False
    cut_on_response: bool = False

    def __init__(self, window, input_device, data_handler, componentSettings):
        self.window = window
        self.input_device = input_device
        self.data_handler = data_handler

        if "response" in componentSettings:
            self.response = ResponseComponent(componentSettings["response"])
        
        if "visual_components" in componentSettings:
            for component in componentSettings["visual_components"]:
                self.visual.append(VisualComponent(window, component))
        
        if "audio_components" in componentSettings:
            for component in componentSettings["audio_components"]:
                self.audio.append(AudioComponent(window, component))
        
        if "wait_components" in componentSettings:
            for component in componentSettings["wait_components"]:
                self.wait.append(WaitComponent(component))

    def _get_all_components(self) -> list[BaseComponent]:
        return [
            self.response,
            *self.visual,
            *self.audio,
            *self.wait,
        ]
    
    def _refresh(self):
        for component in self._get_all_components():
            component.refresh()
    
    def run(self, trial_values: dict, debug_data = False):
        self._refresh()

        for component in self._get_all_components():
            component.prepare(trial_values)

        for key, value in trial_values.items():
            self.data_handler.addData(key, r"{}".format(value))

        running = True
        self.clock.reset(-self.window.getFutureFlipTime(clock="now"))
        
        while running:
            if input_device.getKeys(["escape"]):
                return False
            
            time = self.clock.getTime()
            thisFlip = self.window.getFutureFlipTime(clock=self.clock)
            thisFlipGlobal = self.window.getFutureFlipTime(clock=None)

            running = False

            for component in self._get_all_components():
                if component.not_started():
                    if thisFlip >= component.start_time - FRAMETOLERANCE:
                        component.start(time, thisFlipGlobal)
                elif component.started():
                    if thisFlip >= component.stop_time - FRAMETOLERANCE:
                        if debug_data:
                            component.stop(time, thisFlipGlobal, self.data_handler)
                        else:
                            component.stop(time, thisFlipGlobal)
                
                if not component.finished():
                    running = True

            self.response.check(input_device, self.data_handler)

            if self.wait_for_response and not self.response.made:
                running = True
            if self.cut_on_response and self.response.made:
                running = False
            
            self.window.flip()
        
        self.data_handler.nextEntry()
        
        return True