from psychopy import clock, logging, core

from conflict_task.constants import *
from conflict_task.devices import Window, InputDevice, DataHandler

from ..component import *

class BaseSequence:
    wait_for_response: bool = False
    cut_on_response: bool = False

    def __init__(self, window, input_device, data_handler, componentSettings):
        self.window: Window = window
        self.input_device: InputDevice = input_device
        self.data_handler: DataHandler = data_handler

        self.response: ResponseComponent = None
        self.visual: list[VisualComponent] = []
        self.audio: list[AudioComponent] = []
        self.wait: list[WaitComponent] = []

        self.clock: clock.Clock = clock.Clock()

        self.timed: bool = False
        
        if "visual_components" in componentSettings:
            for component in componentSettings["visual_components"].values():
                self.visual.append(VisualComponent(window, component))
        
        if "audio_components" in componentSettings:
            for component in componentSettings["audio_components"].values():
                self.audio.append(AudioComponent(window, component))
        
        if "wait_components" in componentSettings:
            for component in componentSettings["wait_components"].values():
                self.wait.append(WaitComponent(component))
        
        if "response" in componentSettings:
            if "variable" in componentSettings["response"] and "correct_resp" in componentSettings["response"]["variable"]:
                self.response = CorrectResponseComponent(componentSettings["response"])
            else:
                self.response = ResponseComponent(componentSettings["response"])

        if "wait_for_response" in componentSettings:
            self.wait_for_response = bool(componentSettings["wait_for_response"])

        if "cut_on_response" in componentSettings:
            self.cut_on_response = bool(componentSettings["cut_on_response"])
        
        if "timed" in componentSettings:
            self.timed = True

        if self.timed:
            try:
                if "timer" in componentSettings:
                    self.timer = float(componentSettings["timer"])
                else:
                    raise ValueError("If sequence is timed, please provide a timer")
            except ValueError as e:
                logging.fatal(e)
                core.quit()
        
        if (not self.response or not self.cut_on_response) and self.get_duration() == INFINITY:
            logging.fatal("Sequence has no way to finish.")
            core.quit()
    

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

    
    def get_duration(self):
        if self.timed:
            return self.timer
        
        return max([component.stop_time for component in self._get_all_components() if component is not None])


    def refresh(self):
        self._base_sequence_should_not_be_run()

        for component in self._get_all_components():
            component.refresh()


    def prepare_components(self, trial_values):
        for component in self._get_all_components():
            component.prepare(trial_values)


    def run_frame(self, debug_data = False, allow_escape = True):
        # Check if user wants to quit experiment
        if allow_escape and self.input_device.was_key_pressed("escape"):
            return QUIT_EXPERIMENT
        

        # Get current timers
        time = self.clock.getTime()
        thisFlip = self.window.getFutureFlipTime(clock=self.clock)
        thisFlipGlobal = self.window.getFutureFlipTime(clock=None)


        # Return variable is whether or not to continue the sequence
        keep_running = STOP_RUNNING


        # Iterate through components
        for component in self._get_all_components():

            # Either start them...
            if component.not_started():
                if thisFlip >= component.start_time - FRAMETOLERANCE:
                    component.start(time, thisFlip, thisFlipGlobal)
            # ...or stop them
            elif component.started():
                if thisFlip >= component.stop_time - FRAMETOLERANCE:
                    if debug_data:
                        component.stop(time, thisFlip, thisFlipGlobal, self.data_handler)
                    else:
                        component.stop(time, thisFlip, thisFlipGlobal)
            
            # If not all components have finished, continue the sequence
            if not component.finished():
                keep_running = KEEP_RUNNING


        # If sequence has a response component check for it 
        if self.response:
            self.response.check(self.input_device, self.data_handler)
            
            # Two possibilities based on the response settings
            if self.response.made:
                if self.cut_on_response:
                    # Cutting sequence short after a response has been made
                    keep_running = STOP_RUNNING
            else:
                if self.wait_for_response:
                    # Wait for response even though all components have finished
                    keep_running = KEEP_RUNNING
        
        
        # Finally, if timed check if sequence has finished it's timer
        if self.timed:
            if thisFlip >= self.timer:
                keep_running = STOP_RUNNING
        

        # Flip window
        self.window.flip()


        # Continue sequence or not
        return keep_running


    def run(self, trial_values: dict = {}, debug_data = False):
        self._base_sequence_should_not_be_run()

        self.refresh()
        self.prepare_components(trial_values)

        self.data_handler.add_data_dict(trial_values)
        self.clock.reset(-self.window.getFutureFlipTime(clock="now"))

        running = KEEP_RUNNING
        
        while running == KEEP_RUNNING:
            running = self.run_frame(debug_data)

            if running == QUIT_EXPERIMENT:
                return False
        
        self.data_handler.next_entry()
        
        return True