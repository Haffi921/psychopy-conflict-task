from psychopy import logging, core

from .base_component import BaseComponent

class ResponseComponent(BaseComponent):
    name = "response"
    inputDevice = None

    keys: list = None
    variable_factor: dict = None

    correct_resp = None
    made: bool = False
    key: str = None
    rt: float = None
    correct: bool = None

    def __init__(self, component_settings):
        super().__init__(component_settings)
        
        try:
            if "keys" in component_settings and len(component_settings["keys"]):
                self.keys = component_settings["keys"]
            else:
                raise ValueError("Valid repsonse keys are not specified")

            if "variable" in component_settings:
                self.variable_factor = component_settings["variable"]
            
            if "correct_resp" not in self.variable_factor:
                raise ValueError("'correct_resp' must be a key in variable factors of ResponseComponent")
        except ValueError as e:
            logging.fatal(e)
            core.quit()

    def refresh(self):
        super().refresh()
        self.correct_resp = None
        self.made = False
        self.key = None
        self.rt = None
        self.correct = None

        for factor_name, _ in self.variable_factor.items():
            if factor_name == "correct_resp":
                continue
            setattr(self, factor_name, None)
    
    def prepare(self, trial_values: dict):
        for factor_name, factor_id in self.variable_factor.items():
            try:
                if factor_id in trial_values.keys():
                    setattr(self, factor_name, trial_values[factor_id])
                else:
                    raise KeyError(f"Subject trial sequence does not include key '{factor_id}' required by ResponseComponent")
            except KeyError as e:
                logging.fatal(e)
                core.quit()
    
    def start(self, time, flipTimeGlobal):
        super().start(time, flipTimeGlobal)
    
    def check(self, input_device, dataHandler = None):
        if self.started() and not self.made:
            keyPressed = [(key.name, key.rt) for key in input_device.getKeys(keyList=self.keys)]
            if len(keyPressed):
                self.key, self.rt = keyPressed[-1]
                self.made = True
                if self.key == self.correct_resp:
                    self.correct = True
                else:
                    self.correct = False
                
                if dataHandler:
                    dataHandler.addData(self.name + ".correct_resp", self.correct_resp)
                    dataHandler.addData(self.name + ".made", self.made)
                    dataHandler.addData(self.name + ".key", self.key)
                    dataHandler.addData(self.name + ".rt", self.rt)
                    dataHandler.addData(self.name + ".correct", self.correct)