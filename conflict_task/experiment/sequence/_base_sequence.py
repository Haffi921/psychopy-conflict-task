from psychopy import clock, logging, core

from conflict_task.constants import *
from conflict_task.devices import Window, Keyboard

from ..component import *
from conflict_task.experiment import component

class BaseSequence:

    def __init__(self, window, input_device, sequence_settings):
        self._base_sequence_should_not_be_run()

        self.name: str = "Unnamed Sequence"
        
        self.window: Window = window
        self.input_device: Keyboard = input_device
#        self.data_handler: DataHandler = data_handler

        self.response: ResponseComponent = None
        self.visual: list[VisualComponent] = []
        self.audio: list[AudioComponent] = []
        self.wait: list[WaitComponent] = []

        self.clock: clock.Clock = clock.Clock()

        self.timed: bool = False
        self.wait_for_response: bool = False
        self.cut_on_response: bool = False
        self.takes_trial_values: bool = False
        self.feedback: bool = False
        
        if "name" in sequence_settings:
            if isinstance(sequence_settings["name"], str):
                self.name = sequence_settings["name"]
            else:
                logging.fatal("Sequence name is not a string")

        self._parse_component_settings(sequence_settings)
    

    def _base_sequence_should_not_be_run(self):
        if self.__class__.__name__ == "BaseSequence":
            logging.fatal("An instance of BaseSequence should not be created nor run")
            core.quit()
    

    def _create_components(self, component_settings, component_class: BaseComponent, *args, **kwargs):
        settings: list = None
        components: list = []

        if isinstance(component_settings, list):
            settings = component_settings    
        elif isinstance(component_settings, dict):
            settings = list(component_settings.values())
        else:
            logging.fatal(f"Sequence components must listed either in a dictionary or as a list")
            core.quit()
        
        for component in settings:
            components.append(component_class(component, *args, **kwargs))

        return components
    

    def _parse_component_settings(self, sequence_settings: dict):
        if "visual_components" in sequence_settings:
            self.visual = self._create_components(
                sequence_settings["visual_components"], VisualComponent, self.window
            )
        
        if "audio_components" in sequence_settings:
            self.audio = self._create_components(
                sequence_settings["audio_components"], AudioComponent, self.window
            )
        
        if "wait_components" in sequence_settings:
            self.wait = self._create_components(
                sequence_settings["wait_components"], WaitComponent
            )
        

        if response := sequence_settings.get("response"):
            if "correct_key" in response.get("variable", {}):
                self.response = CorrectResponseComponent(response)
            else:
                self.response = ResponseComponent(response)

        elif response := sequence_settings.get("correct_response"):
            self.response = CorrectResponseComponent(response)
    

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

    
    def get_data(self):
        data = {}

        for component in self._get_all_components():
            data = data | component.get_data()
        
        return data


    def run_frame(self, allow_escape = False):
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
                    component.stop(time, thisFlip, thisFlipGlobal)
            
            # If not all components have finished, continue the sequence
            if not component.finished():
                keep_running = KEEP_RUNNING


        # If sequence has a response component check for it 
        if self.response:
            self.response.check(self.input_device)
            
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


    def run(self, trial_values: dict = {}, allow_escape = False):
        self._base_sequence_should_not_be_run()

        self.refresh()
        if self.takes_trial_values:
            self.prepare_components(trial_values)

        self.clock.reset(-self.window.getFutureFlipTime(clock="now"))
        self.input_device.reset_clock()

        running = KEEP_RUNNING
        
        while running == KEEP_RUNNING:
            running = self.run_frame(allow_escape = allow_escape)

            if running == QUIT_EXPERIMENT:
                return False
        
        return True