from psychopy import core, logging
from psychopy.constants import NOT_STARTED, STARTED, FINISHED

class BaseComponent:
    name = "UNKNOWN_COMPONENT"
    """Name of component for data registration."""

    variable_factor: dict = None
    """Dictionary of component member variables that will be different each sequence"""


    start_time: float = 0.0
    """Start time for component relative to sequence start."""

    stop_time: float = 0.0
    """Stop time for component relative to sequence start."""


    status = NOT_STARTED
    """Component status (NOT_STARTED, STARTED, FINISHED)"""
    
    time_started: float = None
    """Time that component started, relative to sequence start."""

    time_started_refresh: float = None
    """Screen flip time that component started, relative to sequence start."""

    time_started_global: float = None
    """Time that component started, relative to experiment start."""

    time_stopped = None
    """Time that component stopped, relative to sequence start."""

    time_stopped_refresh = None
    """Screen flip time that component stopped, relative to sequence start."""

    time_stopped_global: float = None
    """Time that component stopped, relative to experiment start."""


    drawable = False
    """True if component is a visual component, false if not."""


    def __init__(self, component_settings):
        """
        Takes in a `component_settings` dictionary to set up component variables.

        For all components, settings are as follows:

            1) `start`          (float): Start time for component relative to sequence start. (Required)

            2) End time, either through: (Optional)
                a) `stop`       (float): Stop time for component relative to sequence start.
                b) `duration`   (float): Length of time between component's start and stop.
                Behind the scenes `stop` = `start` + `duration`.

            3) `variable`        (dict): Component member variables that will be different each sequence.
        """

        try:
            if "start" in component_settings:
                self.start_time = component_settings["start"]
            else:
                raise ValueError("Component must have a start time")
            
            if "stop" in component_settings.keys():
                self.stop_time = component_settings["stop"]
                
                if self.stop_time < self.start_time:
                    raise ValueError("Component stop time must not be less than the start time")

            elif "duration" in component_settings.keys():
                self.stop_time = self.start_time + component_settings["duration"]

            else:
                raise ValueError("Component must have an end time - either 'stop' or 'duration'.")
            
            if "variable" in component_settings:
                self.variable_factor = component_settings["variable"]

        except ValueError as e:
            logging.fatal(e)
            core.quit()


    def refresh(self):
        """
        Used before each component use.
        
        For all components, this refreshes `status`, `time_started`, `time_started_refresh`,
        `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.
        """

        self.status = NOT_STARTED
        self.time_started = None
        self.time_started_refresh = None
        self.time_started_global = None
        self.time_stopped = None
        self.time_stopped_refresh = None
        self.time_stopped_global = None
    

    def prepare(self, trial_values: dict, component, component_info: str):
        """
        Sets the key-value pairs from `trial_values` on the component.

        Args:
            
            `trial_values`   (dict): Dictionary of key-value pairs that link up component member variables (keys) with their respective values.

            `component`       (Any): The object on which the `trial_values` are enacted on. Most cases it will be `self`.

            `component_info`  (str): Component information string for logging and debug purposes.
        """

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


    def start(self, time, flipTime, timeGlobal):
        """
        Starts component and records time.

        Args:

            `time`        (float): Time relative to sequence start.

            `flipTime`    (float): Screen flip time relative to sequence start.

            `timeGlobal`  (float): Time relative to experiment start.
        """

        self.time_started = time
        self.time_started_refresh = flipTime
        self.time_started_global = timeGlobal
        self.status = STARTED
    

    def stop(self, time, flipTime, timeGlobal, dataHandler = None):
        """
        Stops component and records time.

        Args:
        
            `time`                     (float): Time relative to sequence start.

            `flipTime`                 (float): Screen flip time relative to sequence start.

            `timeGlobal`               (float): Time relative to experiment start.

            `data_handler` (ExperimentHandler): Instance of an ExperimentHandler to record data.
        """

        self.time_stopped = time
        self.time_stopped_refresh = flipTime
        self.time_stopped_global = timeGlobal
        self.status = FINISHED

        if dataHandler:
            dataHandler.addData(self.name + ".time_started", self.time_started)
            dataHandler.addData(self.name + ".time_started_refresh", self.time_started_refresh)
            dataHandler.addData(self.name + ".time_started_global", self.time_started_global)
            dataHandler.addData(self.name + ".time_stopped", self.time_stopped)
            dataHandler.addData(self.name + ".time_stopped_refresh", self.time_stopped_refresh)
            dataHandler.addData(self.name + ".time_stopped_global", self.time_stopped_global)
    

    def not_started(self):
        """
        Returns True if component has not been started, false if not.
        """

        return self.status == NOT_STARTED
    
    def started(self):
        """
        Returns True if component has been started, false if not.
        """

        return self.status == STARTED
    
    def finished(self):
        """
        Returns True if component has finished, false if not.
        """

        return self.status == FINISHED