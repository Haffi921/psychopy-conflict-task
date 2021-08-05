import os
from sys import path
from psychopy.data import ExperimentHandler

thisDir = os.path.abspath(path[0])

data_handler = ExperimentHandler(dataFileName="test")

# def add(key, value):
#     data_handler.addData(key, str(value).encode("unicode_escape").decode())
# add("Hello", "World\nWorld\nWorld")
# data_handler.nextEntry()
# add("Hello", 3)

# data_handler.nextEntry()

from conflict_task.devices import Window, Keyboard
from conflict_task.experiment.screen.information_screen import InformationScreen

window_settings = dict(

    # Size of the window in pixels (x, y)
    size = (1920, 1200),

    # Color of background as [r, g, b] list or single value. Each gun can take values between -1.0 and 1.0
    color = [0, 0, 0],

    # Create a window in ‘full-screen’ mode. Better timing can be achieved in full-screen mode
    fullscreen = True,

    # If not fullscreen, then position of the top-left corner of the window on the screen (x, y)
    pos = (0, 0),

    # Which monitor? 0 is primary monitor, 1 is secondary, etc.
    screen = 0,

    #---- Rest are less useful settings to tinker with, so it's not recommended ----#
    monitor='testMonitor',

    # Set the window type or back-end to use
    winType = 'pyglet',

    # Use framebuffer object
    useFBO = True,

    # Defines the default units of stimuli drawn in the window (can be overridden by each stimulus).
    # Values can be None, ‘height’ (of the window), ‘norm’ (normalised), ‘deg’, ‘cm’, ‘pix’
    units = 'height'
)

componentSettings = dict(
    visual_components = dict(
        text = dict(
            name = "text",
            type = "TextStim",
            spec = dict(
                name = "target",
                color = "white",
                height = 0.02,
                text = "Hello!"
            )
        )
    )
)

window = Window(window_settings)
input_device = Keyboard().device
screen = InformationScreen(window, input_device, data_handler, componentSettings)

screen.run()

data_handler.saveAsWideText(thisDir + os.sep + "test.csv")
data_handler.abort()