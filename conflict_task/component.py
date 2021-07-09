from psychopy import visual, core
from psychopy.constants import NOT_STARTED, STARTED, FINISHED

class BaseComponent:
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

    def start(self, time, flipTimeGlobal):
        self.time_started = time
        self.time_started_refresh = flipTimeGlobal
        self.status = STARTED
    
    def stop(self, time, flipTimeGlobal):
        self.time_stopped = time
        self.time_stopped_refresh = flipTimeGlobal
        self.status = FINISHED
    
    def not_started(self):
        return self.status == NOT_STARTED
    
    def started(self):
        return self.status == STARTED
    
    def finished(self):
        return self.status == FINISHED

class ResponseComponent(BaseComponent):
    keys = []

    made = False
    key = None
    correct_key = None
    rt = None
    correct = None

    def __init__(self, component_settings):
        super().__init__(component_settings)
        
        if "keys" in component_settings and len(component_settings["keys"]):
            self.keys = component_settings["keys"]
        else:
            print("Valid repsonse keys are not specified")
            core.quit()

    def refresh(self):
        super().refresh()
        self.made = False
        self.key = None
        self.correct_key = None
        self.rt = None
        self.correct = None
    
    def set_correct_key(self, index):
        self.correct_key = self.keys[index]
    
    def check(self, input_device):
        if self.started() and not self.made:
            keyPressed = [(key.name, key.rt) for key in input_device.getKeys(keyList=self.keys)]
            if len(keyPressed):
                self.key, self.rt = keyPressed[-1]
                self.made = True
                if self.key == self.correct_key:
                    self.correct = True
                else:
                    self.correct = False

class VisualComponent(BaseComponent):
    visual = None

    alternating = False

    variable_factor = None

    def __init__(self, window, component_settings: dict):
        super().__init__(component_settings)

        type = component_settings["type"]
        if hasattr(visual, type):
            self.visual = getattr(visual, type)(window, **component_settings["spec"])
        else:
            print(f"There's no visual component type {type}")
            core.quit()
        
        self.drawable = True
        
        if "random" in component_settings:
            self.variable_factor = component_settings["random"]
            variable_list = list(self.variable_factor.values())
            self.variable_factor["random_max"] = len(variable_list[0])
        elif "alternating" in component_settings:
            self.alternating = True
            self.variable_factor = component_settings["alternating"]["random"]
            variable_list = list(self.variable_factor.values())
            self.variable_factor["alternating_max"] = len(variable_list[0])
            self.variable_factor["random_max"] = len(variable_list[0][0])
    
    def prepare(self, random = 0, alternating = 0):
        factor_name, factor_values = list(self.variable_factor.items())[0]
        if self.alternating:
            factor_value = factor_values[alternating][random]
        else:
            factor_value = factor_values[random]
        
        setattr(self.visual, factor_name, factor_value)

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
    
    def stop(self, time, flipTimeGlobal):
        super().stop(time, flipTimeGlobal)
        self.turnAutoDrawOff()
