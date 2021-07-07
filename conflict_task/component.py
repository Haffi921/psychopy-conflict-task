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
        
        if "keys" in component_settings:
            self.keys = [component_settings["keys"]]
        elif "alternating" in component_settings:
            if "keys" in component_settings["alternating"]:
                self.keys = component_settings["alternating"]["keys"]
        
        if len(self.keys) == 0:
            print("Response has no keys")
            core.quit()


    def refresh(self):
        super().refresh()
        self.made = False
        self.key = None
        self.correct_key = None
        self.rt = None
        self.correct = None
    
    def check(self, input_device, alternating = 0):
        if self.started() and not self.made:
            keyPressed = [(key.name, key.rt) for key in input_device.getKeys(keyList=self.keys[alternating])]
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
    random = False
    variable_factor: dict = None

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
            self.random = True
            self.variable_factor = component_settings["random"]
        elif "alternating" in component_settings:
            self.alternating = True
            if "random" in component_settings["alternating"]:
                self.random = True
                self.variable_factor = component_settings["alternating"]["random"]
            else:
                self.variable_factor = component_settings["alternating"]
    
    def prepare(self, random = 0, alternating = 0):
        if self.alternating or self.random:
            factor_name, factor_values = dict(self.variable_factor.items())[0]
            if self.alternating and self.random():
                factor_value = factor_values[alternating][random]
            elif self.alternating:
                factor_value = factor_values[alternating]
            elif self.random:
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
