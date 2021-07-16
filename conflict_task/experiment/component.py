from psychopy import visual, core, logging
from psychopy.constants import NOT_STARTED, STARTED, FINISHED

class BaseComponent:
    name = "UNKNOWN_COMPONENT"

    start_time = 0
    stop_time = 0

    status = NOT_STARTED
    time_started = None
    time_started_refresh = None
    time_stopped = None
    time_stopped_refresh = None

    drawable = False

    def __init__(self, component_settings):
        self.start_time = component_settings["start"]
        
        if "stop" in component_settings.keys():
            self.stop_time = component_settings["stop"]
        elif "duration" in component_settings.keys():
            self.stop_time = self.start_time + component_settings["duration"]

    def refresh(self):
        self.status = NOT_STARTED
        self.time_started = None
        self.time_started_refresh = None
        self.time_stopped = None
        self.time_stopped_refresh = None
    
    def prepare(self, trial_values: dict):
        logging.fatal("'prepare' method BaseComponent should never be invoked")
        core.quit()

    def start(self, time, flipTimeGlobal):
        self.time_started = time
        self.time_started_refresh = flipTimeGlobal
        self.status = STARTED
    
    def stop(self, time, flipTimeGlobal, dataHandler = None):
        self.time_stopped = time
        self.time_stopped_refresh = flipTimeGlobal
        self.status = FINISHED

        if dataHandler:
            dataHandler.addData(self.name + ".time_started", self.time_started)
            dataHandler.addData(self.name + ".time_started_refresh", self.time_started_refresh)
            dataHandler.addData(self.name + ".time_stopped", self.time_stopped)
            dataHandler.addData(self.name + ".time_stopped_refresh", self.time_stopped_refresh)
    
    def not_started(self):
        return self.status == NOT_STARTED
    
    def started(self):
        return self.status == STARTED
    
    def finished(self):
        return self.status == FINISHED

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

    def __init__(self, component_settings, inputDevice):
        super().__init__(component_settings)

        self.inputDevice = inputDevice
        
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
        self.inputDevice.clock.reset()
    
    def check(self, dataHandler = None):
        if self.started() and not self.made:
            keyPressed = [(key.name, key.rt) for key in self.input_device.getKeys(keyList=self.keys)]
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
