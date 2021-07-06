from psychopy import visual

def create_window(window_settings):
    if window_settings["fullscreen"]:
        return visual.Window(
            size = window_settings["size"],
            color = window_settings["color"],
            fullscreen = True,
            screen = window_settings["screen"],
            winType = window_settings["winType"],
            useFBO = window_settings["useFBO"],
            units = window_settings["units"]
        )
    else:
        return visual.Window(
            size = window_settings["size"],
            color = window_settings["color"],
            pos = window_settings["pos"],
            screen = window_settings["screen"],
            winType = window_settings["winType"],
            useFBO = window_settings["useFBO"],
            units = window_settings["units"]
        )

class Window:
    
    window_settings = None