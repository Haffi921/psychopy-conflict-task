from psychopy import logging, core

from .base_component import BaseComponent

class ResponseComponent(BaseComponent):
    """
    Component to record user input through an InputDevice.

    Records the key that a user responds with and the reaction time.
    """


    name = "input"

    keys: list = None
    """List of keys that users are allowed to responde with."""

    made: bool = False
    """True if user has responded. Refreshes with `ResponseComponent.refresh()`."""

    key: str = None
    """The key that a user responds with. Refreshes with `ResponseComponent.refresh()`."""

    rt: float = None
    """The response time. Refreshes with `ResponseComponent.refresh()`."""


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

        ------------------------------------------

        ResponseComponent's settings must include:

            `keys`    (list): List of keys that users are allowed to responde with.
        """

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
        """
        Used before each component use.
        
        For all components, this refreshes `status`, `time_started`, `time_started_refresh`,
        `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.

        For a ResponseComponent, this refreshes variables `made`, `key` and `rt`.
        """

        super().refresh()

        self.made = False
        self.key = None
        self.rt = None


    def prepare(self, trial_values: dict, component_info: str = "InputComponent"):
        """
        Sets the key-value pairs from `trial_values` on the ResponseComponent.

        Args:

            `trial_values`   (dict): Dictionary of key-value pairs that link up component member variables (keys) with their respective values.

            `component_info`  (str): Component information string for logging and debug purposes.
        """

        super().prepare(trial_values, self, component_info)


    def check(self, input_device, data_handler = None):
        """
        Checks for input using `input_device` and logs data using `data_handler`.
        
        Uses `ResponseComponent.keys` list as input possiblities. If user presses any of the keys from this list:

            1) `made` becomes True

            2) `key` and `rt` are recorded

            3) `data_handler` records `made`, `key` and `rt`
        
        Args:

            `input_device`        (InputDevice): Device used to check input. Can be Keyboard or any Parallel port device.

            `data_handler`  (ExperimentHandler): Instance of an ExperimentHandler to record data.

        Returns:

            Keypress tuple (str, float): Tuple with key and reaction time.
        """
        
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
    """
    Component to record user input through an InputDevice and compare to a correct response.

    Records the key that a user responds with, the reaction time and correctness.
    """

    name = "response"
    
    correct_resp = None
    """String of the correct repsonse key"""

    correct: bool = None
    """True if response key is correct"""


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

        ------------------------------------------

        ResponseComponent's settings must include:

            `keys`    (list): List of keys that users are allowed to responde with.
        
        ------------------------------------------

        CorrectResponseComponent's settings must have `correct_resp` (str) as a variable factor.
        """

        super().__init__(component_settings)
        
        try:     
            if "correct_resp" not in self.variable_factor:
                raise ValueError("'correct_resp' must be a key in variable factors of ResponseComponent")
        except ValueError as e:
            logging.fatal(e)
            core.quit()


    def refresh(self):
        """
        Used before each component use.
        
        For all components, this refreshes `status`, `time_started`, `time_started_refresh`,
        `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.

        For a ResponseComponent, this refreshes variables `made`, `key` and `rt`.
        
        For a CorrectResponseComponent, this refreshes variables `correct_resp` and `correct`.
        """

        super().refresh()
        
        self.correct_resp = None
        self.correct = None

        # for factor_name, _ in self.variable_factor.items():
        #     if factor_name == "correct_resp":
        #         continue
        #     setattr(self, factor_name, None)
    

    def prepare(self, trial_values: dict):
        """
        Sets the key-value pairs from `trial_values` on the ResponseComponent.

        Args:

            `trial_values`   (dict): Dictionary of key-value pairs that link up component member variables (keys) with their respective values.
        """

        super().prepare(trial_values, self, "ResponseComponent")
    

    def check(self, input_device, data_handler = None):
        """
        Checks for input using `input_device` and logs data using `data_handler`. \n
        
        Uses `ResponseComponent.keys` list as input possiblities. If user presses any of the keys from this list:

            1) `made` becomes True.

            2) `key` and `rt` are recorded.
            
            3) `correct` becomes True if `key` == `correct_resp`, and False if `key` != `correct_resp`.

            4) `data_handler` records `made`, `key`, `rt`, `correct_resp` and `correct`.
        
        Args:

            `input_device`        (InputDevice): Device used to check input. Can be Keyboard or any Parallel port device.

            `data_handler`  (ExperimentHandler): Instance of an ExperimentHandler to record data.
        """

        super().check(input_device, data_handler)

        if self.started() and not self.made:
            if self.key == self.correct_resp:
                self.correct = True
            else:
                self.correct = False
            
            if data_handler:
                data_handler.addData(self.name + ".correct_resp", self.correct_resp)
                data_handler.addData(self.name + ".correct", self.correct)