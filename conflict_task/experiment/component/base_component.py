from psychopy import core, logging
from psychopy.constants import NOT_STARTED, STARTED, FINISHED

class BaseComponent:
    name = "UNKNOWN_COMPONENT"

    variable_factor: dict = None

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
        
        if "variable" in component_settings:
            self.variable_factor = component_settings["variable"]

    def refresh(self):
        self.status = NOT_STARTED
        self.time_started = None
        self.time_started_refresh = None
        self.time_stopped = None
        self.time_stopped_refresh = None
    
    def prepare(self, trial_values: dict, component, component_info: str):
        if self.__class__.__name__ == "BaseComponent":
            logging.fatal("'prepare' method BaseComponent should never be invoked")
            core.quit()
        if self.variable_factor:
            for factor_name, factor_id in self.variable_factor.items():
                try:
                    if factor_id in trial_values.keys():
                        setattr(component, factor_name, trial_values[factor_id])
                    else:
                        raise KeyError(f"Subject trial sequence does not include key '{factor_id}' required by {component_info}")
                except KeyError as e:
                    logging.fatal(e)
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