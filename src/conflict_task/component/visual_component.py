from psychopy import visual

from conflict_task.util import *

from ._base_component import BaseComponent


class VisualComponent(BaseComponent):
    """
    Component to display a visual stimulus on screen.

    Basically this is a wrapper for all of PsychoPy's visual stimuli.
    """

    def __init__(self, component_settings: dict, window) -> None:
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
        # VisualComponent Initialization
        # -----------------------------------------------
        super().__init__(component_settings)

        if name := get_type(component_settings, "name", str):
            self.name = name
        elif spec_name := get_type(component_settings, "spec", dict, {}).get("name"):
            self.name = spec_name
        else:
            fatal_exit(
                "Please specify a name for each VisualComponent, either at top level or in spec\n"
                + f"Here are the unnamed settings: {component_settings}"
            )

        visual_type = get_type_or_fatal_exit(
            component_settings,
            "type",
            str,
            f"{self.name}: VisualComponents must specify a 'type'",
        )
        true_or_fatal_exit(
            hasattr(visual, visual_type),
            f"{self.name}: There's no visual component type {visual_type}",
        )

        visual_spec: dict = get_type_or_fatal_exit(
            component_settings,
            "spec",
            dict,
            f"{self.name}: VisualComponents require specifications - use 'spec' field",
        )

        self.component: visual.TextStim = getattr(visual, visual_type)(
            window, **visual_spec
        )
        # -----------------------------------------------

    def refresh(self) -> None:
        """
        Used before each component use.

        For all components, this refreshes `status`, `time_started`, `time_started_refresh`, `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.

        For VisualComponent, this also turns off AutoDraw.
        """

        super().refresh()
        self._turn_auto_draw_off()

    def _turn_auto_draw_on(self) -> None:
        """
        Turns AutoDraw on for the visual stimulus connected to this component.

        AutoDraw means that the component is automatically drawn before each screen flip.
        If not turned on, visual stimulus must be explicitly drawn before each frame.
        """

        self.component.setAutoDraw(True)

    def _turn_auto_draw_off(self) -> None:
        """
        Turns AutoDraw off for the visual stimulus connected to this component.

        AutoDraw means that the component is automatically drawn before each screen flip.
        If not turned on, visual stimulus must be explicitly drawn before each frame.
        """

        self.component.setAutoDraw(False)

    def start(self, time, time_flip, global_flip) -> None:
        """
        Starts component and records time.

        Args:

            `time`        (float): Time relative to sequence start.

            `time_flip`    (float): Screen flip time relative to sequence start.

            `global_flip`  (float): Time relative to experiment start.

        For a VisualComponent, this also turns on AutoDraw.
        """

        super().start(time, time_flip, global_flip)
        self._turn_auto_draw_on()

    def stop(self, time, time_flip, global_flip) -> None:
        """
        Stops component and records time.

        Args:

            `time`                     (float): Time relative to sequence start.

            `time_flip`                 (float): Screen flip time relative to sequence start.

            `global_flip`               (float): Time relative to experiment start.

        For a VisualComponent, this also turns off AutoDraw.
        """

        super().stop(time, time_flip, global_flip)
        self._turn_auto_draw_off()
