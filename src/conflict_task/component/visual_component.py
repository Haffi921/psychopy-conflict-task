from psychopy import visual

from conflict_task.devices import Window
from conflict_task.util import *

from ._base_component import BaseComponent


class VisualComponent(BaseComponent):
    """
    Component to display a visual stimulus on screen.

    Basically this is a wrapper for all of PsychoPy's visual stimuli.
    """

    def __init__(self, component_settings: dict) -> None:
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

        self.type = get_type_or_fatal_exit(
            component_settings,
            "type",
            str,
            f"{self.name}: VisualComponents must specify a 'type'",
        )

        self.create_visual_component(component_settings)
        # true_or_fatal_exit(
        #     hasattr(visual, visual_type),
        #     f"{self.name}: There's no visual component type {visual_type}",
        # )
        # -----------------------------------------------

    def create_visual_component(self, component_settings):
        visual_spec: dict = get_type(component_settings, "spec", dict, {})

        if self.type == "text":
            if self.variable_factor and "size" in self.variable_factor:
                self.variable_factor["height"] = self.variable_factor["size"]
                del self.variable_factor["size"]
            self.component = self.create_text_component(visual_spec)
        
        elif self.type == "image":
            self.preload = None
            if "preload" in component_settings:
                self.preload = {}
                for image in component_settings["preload"]:
                    self.preload[image] = self.create_image_component({
                            **visual_spec,
                            "image": image,
                        })
            
            if "image" in visual_spec and self.preload:
                if (image := visual_spec["image"]) in self.preload:
                    self.component = self.preload[image]
                else:
                    self.component = self.create_image_component(visual_spec)
                    self.preload[image] = self.component
            else:
                self.component = self.create_image_component(visual_spec)
        
        else:
            if self.type == "shape":
                self.type = "ShapeStim"
            visual_spec["size"] = Window.pix2norm_size(visual_spec["size"])
            self.component = self.create_other_component(self.type, visual_spec)

    @staticmethod
    def create_text_component(spec_settings):
        if "size" in spec_settings:
            spec_settings["height"] = Window.pt2norm_size(spec_settings["size"])
            del spec_settings["size"]

        return visual.TextStim(Window._window, **spec_settings)


    @staticmethod
    def create_image_component(spec_settings):
        return visual.TextStim(Window._window, **spec_settings)

    @staticmethod
    def create_other_component(type, spec_settings):
        if hasattr(visual, type):
            return getattr(visual, type)(Window._window, **spec_settings)
        else:
            fatal_exit(f"No component named {type}")

    def refresh(self) -> None:
        """
        Used before each component use.

        For all components, this refreshes `status`, `time_started`, `time_started_refresh`, `time_started_global`, `time_stopped`, `time_stopped_refresh` and `time_stopped_global`.

        For VisualComponent, this also turns off AutoDraw.
        """

        super().refresh()
        self._turn_auto_draw_off()
    
    def prepare(self, trial_values: dict) -> None:
        if self.variable_factor:
            if self.type == "text":
                ## Dirty hack for a stupid bug
                if "text" in self.variable_factor:
                    self.component.text = ""  # Value needs to be forcefully changed for other attributes to take effect
                if "size" in self.variable_factor:
                    trial_values["height"] = Window.pt2norm_size(trial_values["size"])
            elif "size" in self.variable_factor:
                if self.type in ["shape", "Rect", "Circle", "Polygon", "Line", "Pie"]:
                    trial_values["size"] = Window.pix2norm_size(trial_values["size"])
            
            if self.type == "image":
                if "image" in trial_values and self.preload:
                    image = trial_values["image"]
                    self.component = self.preload[image]
                    del trial_values["image"]
                    super().prepare(trial_values)
                    trial_values["image"] = image
            
            else:
                super().prepare(trial_values)


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
        self.send_marker_value()

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


class TextComponent(VisualComponent):
    def __init__(self, component_settings: dict) -> None:
        super().__init__(component_settings)

        visual_spec: dict = get_type(component_settings, "spec", dict, {})

        self.handle_size_height(self.variable_factor)
        self.handle_size_height(visual_spec, Window.pt2norm_size)
        
        self.component = visual.TextStim(Window._window, **visual_spec)

    @staticmethod
    def handle_size_height(dictionary: dict, func = None):
        if dictionary and "size" in dictionary:
            size = dictionary["size"] if not func else func(dictionary["size"])
            dictionary["height"] = size
            del dictionary["size"]

    def prepare(self, trial_values: dict) -> None:
        # Dirty hack for a stupid bug
        if "text" in self.variable_factor:
            # Value needs to be forcefully changed for other attributes to take effect
            self.component.text = ""

        if "size" in self.variable_factor:
            trial_values["height"] = Window.pt2norm_size(trial_values["size"])
        
        super().prepare(trial_values)
    

class ImageComponent(VisualComponent):
    def __init__(self, component_settings: dict) -> None:
        self.preload = None

        super().__init__(component_settings)
        visual_spec: dict = get_type(component_settings, "spec", dict, {})

        if "preload" in component_settings:
            self.preload = {}
            for image in component_settings["preload"]:
                self.preload[image] = visual.ImageStim(Window._window, {
                        **visual_spec,
                        "image": image,
                    })
        
        if "image" in visual_spec and self.preload:
            if (image := visual_spec["image"]) in self.preload:
                self.component = self.preload[image]
            else:
                self.component = visual.ImageStim(Window._window, **visual_spec)
                self.preload[image] = self.component
        else:
            self.component = visual.ImageStim(Window._window, **visual_spec)

    def prepare(self, trial_values: dict) -> None:
        if "image" in trial_values and self.preload:
            image = trial_values["image"]
            self.component = self.preload[image]
            del trial_values["image"]
            super().prepare(trial_values)
            trial_values["image"] = image
        else:
            super().prepare(trial_values)


class ShapeComponent(VisualComponent):
    def __init__(self, component_settings: dict) -> None:
        super().__init__(component_settings)
        visual_spec: dict = get_type(component_settings, "spec", dict, {})

        if self.type == "shape":
            self.type = "ShapeStim"
        elif self.type == "cross":
            self.type = "ShapeStim"
            visual_spec["vertices"] = "cross"
        visual_spec["size"] = Window.pix2norm_size(visual_spec["size"])
        
        if hasattr(visual, self.type):
            self.component = getattr(visual, self.type)(Window._window, **visual_spec)
        else:
            fatal_exit(f"No component named {type}")
    
    def prepare(self, trial_values: dict) -> None:
        if "size" in self.variable_factor:
            trial_values["size"] = Window.pix2norm_size(trial_values["size"])
        
        super().prepare(trial_values)