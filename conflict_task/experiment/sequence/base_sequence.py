from psychopy import clock, logging, core
from psychopy.data import ExperimentHandler

from conflict_task.devices import Window, InputDevice

from ..component import *


FRAMETOLERANCE = 0.001
QUIT_EXPERIMENT = -1
STOP_RUNNING = 0
KEEP_RUNNING = 1

class BaseSequence:
    window: Window
    input_device: InputDevice
    data_handler: ExperimentHandler

    response: ResponseComponent
    visual: list[VisualComponent]
    audio: list[AudioComponent]
    wait: list[WaitComponent]

    clock: clock.Clock

    wait_for_response: bool
    cut_on_response: bool

    def __init__(self, window, input_device, data_handler, componentSettings):
        self.window = window
        self.input_device = input_device
        self.data_handler = data_handler

        self.response = None
        self.visual = []
        self.audio = []
        self.wait = []

        self.clock = clock.Clock()
        
        self.wait_for_response = False
        self.cut_on_response = False
        
        if "visual_components" in componentSettings:
            for component in componentSettings["visual_components"]:
                self.visual.append(VisualComponent(window, component))
        
        if "audio_components" in componentSettings:
            for component in componentSettings["audio_components"]:
                self.audio.append(AudioComponent(window, component))
        
        if "wait_components" in componentSettings:
            for component in componentSettings["wait_components"]:
                self.wait.append(WaitComponent(component))
    
    def _base_sequence_should_not_be_run(self):
        if self.__class__.__name__ == "BaseSequence":
            logging.fatal("An instance of BaseSequence should not be created nor run")
            core.quit()

    def _get_all_components(self) -> list[BaseComponent]:
        self._base_sequence_should_not_be_run()
        
        return [
            self.response,
            *self.visual,
            *self.audio,
            *self.wait,
        ]
    
    def _refresh(self):
        self._base_sequence_should_not_be_run()

        for component in self._get_all_components():
            component.refresh()
    
    def _prepare_components(self, trial_values):
        for component in self._get_all_components():
            component.prepare(trial_values)

    def _run_frame(self, debug_data = False):
        if self.input_device.getKeys(["escape"]):
            return QUIT_EXPERIMENT
            
        time = self.clock.getTime()
        thisFlip = self.window.getFutureFlipTime(clock=self.clock)
        thisFlipGlobal = self.window.getFutureFlipTime(clock=None)

        keep_running = STOP_RUNNING

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
                keep_running = KEEP_RUNNING
        
        if self.response:
            self.response.check(self.input_device, self.data_handler)

            if self.response.made:
                if self.cut_on_response:
                    keep_running = STOP_RUNNING
            else:
                if self.wait_for_response:
                    keep_running = KEEP_RUNNING
        
        self.window.flip()

        return keep_running
    
    def run(self, trial_values: dict, debug_data = False):
        self._base_sequence_should_not_be_run()

        self._refresh()
        self._prepare_components(trial_values)

        # TODO: Put this into it's own class
        for key, value in trial_values.items():
            self.data_handler.addData(key, str(value).encode("unicode_escape").decode())

        running = KEEP_RUNNING
        self.clock.reset(-self.window.getFutureFlipTime(clock="now"))
        
        while running == KEEP_RUNNING:
            running = self._run_frame(debug_data)

            if running == QUIT_EXPERIMENT:
                return False
        
        self.data_handler.nextEntry()
        
        return True