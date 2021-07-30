from psychopy import logging, core

from .base_component import BaseComponent

class ResponseComponent(BaseComponent):
    name = "input"

    keys: list = None

    made: bool = False
    key: str = None
    rt: float = None

    def __init__(self, component_settings):
        super().__init__(component_settings)

        try:
            if "keys" in component_settings and len(component_settings["keys"]):
                self.keys = component_settings["keys"]
            else:
                raise ValueError("Valid input keys are not specified")
        except ValueError as e:
            logging.fatal(e)
            core.quit()

    def refresh(self):
        super().refresh()

        self.made = False
        self.key = None
    
    def prepare(self, trial_values: dict, component, component_info: str = "InputComponent"):
        super().prepare(trial_values, component, component_info)
    
    def check(self, input_device, data_handler = None):
        if self.started() and not self.made:
            key_pressed = [(key.name, key.rt) for key in input_device.getKeys(keyList=self.keys)]
            if len(key_pressed):
                self.key, self.rt = key_pressed[-1]
                self.made = True

                if data_handler:
                    data_handler.addData(self.name + ".made", self.made)
                    data_handler.addData(self.name + ".key", self.key)
                    data_handler.addData(self.name + ".rt", self.rt)
                
                return (self.key, self.rt)
        return (None, None)
    
class CorrectResponseComponent(ResponseComponent):
    name = "response"

    correct_resp = None
    correct: bool = None

    def __init__(self, component_settings):
        super().__init__(component_settings)
        
        try:     
            if "correct_resp" not in self.variable_factor:
                raise ValueError("'correct_resp' must be a key in variable factors of ResponseComponent")
        except ValueError as e:
            logging.fatal(e)
            core.quit()

    def refresh(self):
        super().refresh()
        
        self.correct_resp = None
        self.correct = None

        for factor_name, _ in self.variable_factor.items():
            if factor_name == "correct_resp":
                continue
            setattr(self, factor_name, None)
    
    def prepare(self, trial_values: dict):
        super().prepare(trial_values, self, "ResponseComponent")
    
    def check(self, input_device, data_handler = None):
        super().check(input_device, data_handler)

        if self.started() and not self.made:
            if self.key == self.correct_resp:
                self.correct = True
            else:
                self.correct = False
            
            if data_handler:
                data_handler.addData(self.name + ".correct_resp", self.correct_resp)
                data_handler.addData(self.name + ".correct", self.correct)