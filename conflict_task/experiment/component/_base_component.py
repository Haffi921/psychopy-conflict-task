from psychopy import core, logging

from conflict_task.devices import DataHandler
from conflict_task.constants import *

class BaseComponent:
    """
    TODO: Finish this documentation.
    """

    name = "UNKNOWN_COMPONENT"
    """Name of component for data registration."""

    def __init__(self, component_settings: dict):
        """
        Takes in a `component_settings` dictionary to set up component variables.

        For all components, settings are as follows:

            1) `start`          (float): Start time for component relative to sequence start. Defaults to 0.0.

            2) End time, either through:
                a) `stop`       (float): Stop time for component relative to sequence start.
                b) `duration`   (float): Length of time between component's start and stop.
                Behind the scenes `stop` = `start` + `duration`.
                c) None, which means the component will be displayed indefinitely until the end of the sequence.

            3) `variable`        (dict): Component member variables that will be different each sequence.
        """
        
        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------

        self.variable_factor: dict = None
        """Dictionary of component member variables that will be different each sequence. Default: `None`."""

        self.start_time: float = 0.0
        """Start time for component relative to sequence start. Default: `0.0`."""

        self.stop_time: float = INFINITY
        """Stop time for component relative to sequence start. Default:`Infinity`."""

        self.status: int = NOT_STARTED
        """Component status (NOT_STARTED, STARTED, FINISHED). Defaults: `NOT_STARTED`."""
        
        self.time_started: float = None
        """Time that component started, relative to sequence start.Default: `None`."""

        self.time_started_flip: float = None
        """Screen flip time that component started, relative to sequence start.Default: `None`."""

        self.time_started_global_flip: float = None
        """Screen flip time that component started, relative to experiment start.Default: `None`."""

        self.time_stopped: float = None
        """Time that component stopped, relative to sequence start.Default: `None`."""

        self.time_stopped_flip: float = None
        """Screen flip time that component stopped, relative to sequence start.Default: `None`."""

        self.time_stopped_global_flip: float = None
        """Screen flip time that component stopped, relative to experiment start.Default: `None`."""

        self.drawable: bool = False
        """True if component is a visual component, false if not. Default: `False`."""
        # -----------------------------------------------

        
        # -----------------------------------------------
        # BaseComponent Initialization
        # -----------------------------------------------
        if "start" in component_settings:
            self.start_time = component_settings["start"]
                    
        if "stop" in component_settings:
            self.stop_time = component_settings["stop"]
        elif "duration" in component_settings:
            self.stop_time = self.start_time + component_settings["duration"]

        if "variable" in component_settings:
            self.variable_factor = component_settings["variable"]
        
        try:
            if self.start_time < 0.0:
                raise ValueError("Component start time can not be less than 0.0")
            if self.stop_time < self.start_time:
                raise ValueError("Component stop time must not be less than the start time")
        except ValueError as e:
            logging.fatal(e)
            core.quit()        
        # -----------------------------------------------
    

    def _base_component_should_not_be_run(self):
        if self.__class__.__name__ == "BaseComponent":
            logging.fatal("An instance of BaseComponent should not be created nor run")
            core.quit()


    def refresh(self):
        """
        Refreshes component variables. Perform before each component use.
        
        For all components, this refreshes `status`, `time_started`, `time_started_refresh`,
        `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.
        """

        self._base_component_should_not_be_run()

        self.status = NOT_STARTED
        self.time_started = None
        self.time_started_flip = None
        self.time_started_global_flip = None
        self.time_stopped = None
        self.time_stopped_flip = None
        self.time_stopped_global_flip = None
    

    def prepare(self, trial_values: dict, component = None):
        """
        Sets the key-value pairs from `trial_values` on the component.

        Args:
            
            `trial_values`   (dict): Dictionary of key-value pairs that link up component member variables (keys) with their respective values.

            `component`       (Any): The object on which the `trial_values` are enacted on. Defaults to `self`.

            `component_info`  (str): Component information string for logging and debug purposes.
        """

        self._base_component_should_not_be_run()
        
        if component is None:
            component = self

        if self.variable_factor:
            for factor_name, factor_id in self.variable_factor.items():
                try:
                    if factor_id in trial_values.keys():
                        setattr(component, factor_name, trial_values[factor_id])
                    else:
                        raise KeyError(f"Subject trial sequence does not include key '{factor_id}' required by {self.name}")
                except KeyError as e:
                    logging.fatal(e)
                    core.quit()


    def start(self, time, time_flip, global_flip):
        """
        Starts component and records time.

        Args:

            `time`        (float): Time relative to sequence start.

            `flipTime`    (float): Screen flip time relative to sequence start.

            `timeGlobal`  (float): Screen flip time relative to experiment start.
        """

        self._base_component_should_not_be_run()

        self.time_started = time
        self.time_started_flip = time_flip
        self.time_started_global_flip = global_flip
        self.status = STARTED
    

    def stop(self, time, time_flip, global_flip):
        """
        Stops component and records time.

        Args:
        
            `time`                     (float): Time relative to sequence start.

            `flipTime`                 (float): Screen flip time relative to sequence start.

            `timeGlobal`               (float): Screen flip time relative to experiment start.
        """

        self._base_component_should_not_be_run()

        self.time_stopped = time
        self.time_stopped_flip = time_flip
        self.time_stopped_global_flip = global_flip
        self.status = FINISHED

    def not_started(self):
        """
        Returns True if component has not been started, false if not.
        """

        self._base_component_should_not_be_run()

        return self.status == NOT_STARTED
    
    def started(self):
        """
        Returns True if component has been started, false if not.
        """

        self._base_component_should_not_be_run()

        return self.status == STARTED
    
    def finished(self):
        """
        Returns True if component has finished, false if not.
        """

        self._base_component_should_not_be_run()

        return self.status == FINISHED
    
    def get_data(self) -> dict:
        """
        Returns a dictionary of the component's data
        """
        self._base_component_should_not_be_run()

        return {
            self.name + ".time_started": self.time_started,
            self.name + ".time_started_flip": self.time_started_flip,
            self.name + ".time_started_global_flip": self.time_started_global_flip,
            self.name + ".time_stopped": self.time_stopped,
            self.name + ".time_stopped_flip": self.time_stopped_flip,
            self.name + ".time_stopped_global_flip": self.time_stopped_global_flip,
        }
