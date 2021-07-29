from psychopy import visual, logging, core

from .base_component import BaseComponent

class VisualComponent(BaseComponent):
    visual = None
    name = None
    variable_factor: dict = None

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

        if "variable" in component_settings:
            self.variable_factor = component_settings["variable"]
    
    def prepare(self, trial_values: dict):
        if self.variable_factor:
            for factor_name, factor_id in self.variable_factor.items():
                try:
                    if factor_id in trial_values.keys():
                        setattr(self.visual, factor_name, trial_values[factor_id])
                    else:
                        raise KeyError(f"Subject trial sequence does not include key '{factor_id}' required by VisualComponent '{self.name}'")
                except KeyError as e:
                    logging.fatal(e)
                    core.quit()

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
