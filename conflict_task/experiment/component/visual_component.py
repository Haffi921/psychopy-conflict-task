from psychopy import visual, logging, core

from .base_component import BaseComponent

class VisualComponent(BaseComponent):
    name = None
    visual = None

    def __init__(self, window, component_settings: dict):
        super().__init__(component_settings)

        type = component_settings["type"]
        try:
            if hasattr(visual, type):
                self.visual = getattr(visual, type)(window, **component_settings["spec"])
            else:
                raise ValueError(f"There's no visual component type {type}")
            
            if "name" in component_settings["spec"]:
                self.name = self.visual.name
            else:
                raise ValueError(f"Please specify a name for every VisualComponent in 'spec'")
        except ValueError as e:
            logging.fatal(e)
            core.quit()

        self.drawable = True
    
    def prepare(self, trial_values: dict):
        """
        Sets the key-value pairs from `trial_values` on the VisualComponent.

        Args:
            trial_values   (dict): Dictionary of key-value pairs that link up component member variables (keys) with their respective values.
            component_info  (str): Component information string for logging and debug purposes
        """
        super().prepare(trial_values, self.visual, f"VisualComponent '{self.name}'")

    def turnAutoDrawOn(self):
        self.visual.setAutoDraw(True)
    
    def turnAutoDrawOff(self):
        self.visual.setAutoDraw(False)
    
    def refresh(self):
        super().refresh()
        self.turnAutoDrawOff()

    def start(self, time, flipTimeGlobal):
        super().start(time, flipTimeGlobal)
        self.turnAutoDrawOn()
    
    def stop(self, time, flipTimeGlobal, dataHandler = None):
        super().stop(time, flipTimeGlobal, dataHandler)
        self.turnAutoDrawOff()
