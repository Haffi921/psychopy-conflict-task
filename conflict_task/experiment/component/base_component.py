from psychopy import core, logging
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