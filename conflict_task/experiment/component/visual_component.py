from psychopy import visual, logging, core

from . import BaseComponent

class VisualComponent(BaseComponent):
    """
    Component to display a visual stimulus on screen.

    Basically this is a wrapper for all of PsychoPy's visual stimuli.
    """

    def __init__(self, window, component_settings: dict):
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
        
        ---------------------------------------------

        For a VisualComponent, settings also require:
        
            1) `type`        (str): Name of a PsychoPy visual stimulus type.

            2) `spec`       (dict): Dictionary of arguments to use in creation of visual stimulus.

                - For further information about visual stimuli and their arguments, check out
                the [PsychoPy Website](https://www.psychopy.org/api/visual.html).
            
            3) `name`        (str): Because VisualComponents can be numerous, it's required to give each a name.
        """


        # -----------------------------------------------
        # Class variables
        # -----------------------------------------------
        self.visual: visual.TextStim = None
        """Each VisualComponent is connected to a visual stimulus from PsychoPy. Default: `None`"""

        self.drawable = True
        # -----------------------------------------------


        # -----------------------------------------------
        # VisualComponent Initialization
        # ----------------------------------------------- 
        super().__init__(component_settings)

        try:
            if "name" in component_settings:
                self.name = component_settings["name"]
            elif "spec" in component_settings and "name" in component_settings["spec"]:
                self.name = component_settings["spec"]["name"]
            else:
                raise ValueError(f"Please specify a name for each VisualComponent, \
                    either at top level or in spec")

            if "type" in component_settings:
                type = component_settings["type"]
            else:
                raise ValueError(f"VisualComponents require a type specifier. None found in {self.name}")
            
            if hasattr(visual, type):
                if "spec" in component_settings:
                    self.visual = getattr(visual, type)(window, **component_settings["spec"])
                else:
                    raise ValueError(f"VisualComponents require specifications. None found in {self.name}")
            else:
                raise ValueError(f"There's no visual component type {type}")
        except ValueError as e:
            logging.fatal(e)
            core.quit()
        # -----------------------------------------------


    def refresh(self):
        """
        Used before each component use.
        
        For all components, this refreshes `status`, `time_started`, `time_started_refresh`, `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.

        For VisualComponent, this also turns off AutoDraw.
        """

        super().refresh()
        self._turnAutoDrawOff()


    def prepare(self, trial_values: dict):
        """
        Sets the key-value pairs from `trial_values` on the VisualComponent.

        Args:
            
            `trial_values`   (dict): Dictionary of key-value pairs that link up component member variables (keys) with their respective values.
        """
        super().prepare(trial_values, self.visual)


    def _turnAutoDrawOn(self):
        """
        Turns AutoDraw on for the visual stimulus connected to this component.

        AutoDraw means that the component is automatically drawn before each screen flip.
        If not turned on, visual stimulus must be explicitly drawn before each frame.
        """

        self.visual.setAutoDraw(True)


    def _turnAutoDrawOff(self):
        """
        Turns AutoDraw off for the visual stimulus connected to this component.

        AutoDraw means that the component is automatically drawn before each screen flip.
        If not turned on, visual stimulus must be explicitly drawn before each frame.
        """

        self.visual.setAutoDraw(False)


    def start(self, time, flipTime, timeGlobal):
        """
        Starts component and records time.

        Args:

            `time`        (float): Time relative to sequence start.

            `flipTime`    (float): Screen flip time relative to sequence start.

            `timeGlobal`  (float): Time relative to experiment start.
        
        For a VisualComponent, this also turns on AutoDraw.
        """

        super().start(time, flipTime, timeGlobal)
        self._turnAutoDrawOn()


    def stop(self, time, flipTimeGlobal, dataHandler = None):
        """
        Stops component and records time.

        Args:
        
            `time`                     (float): Time relative to sequence start.

            `flipTime`                 (float): Screen flip time relative to sequence start.

            `timeGlobal`               (float): Time relative to experiment start.

            `data_handler` (ExperimentHandler): Instance of an ExperimentHandler to record data.
        
        For a VisualComponent, this also turns off AutoDraw.
        """

        super().stop(time, flipTimeGlobal, dataHandler)
        self._turnAutoDrawOff()
