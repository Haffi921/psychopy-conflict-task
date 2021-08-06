import os
from sys import path

from conflict_task.devices import Window, Keyboard, DataHandler
from conflict_task.experiment.sequence import Screen

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

text = """
Welcome to this test experiment. Right now you are looking at a Static Information Screen. \
This is to provide you with some information about this experiment and what you should know before starting.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam venenatis accumsan eros a vehicula. Quisque mollis \
ante ac leo tempus egestas ut vitae lectus. Suspendisse maximus venenatis tortor, in imperdiet ipsum rutrum quis. \
Nulla quis est in mauris feugiat cursus feugiat nec tellus. Quisque a purus iaculis, commodo nibh id, pharetra odio. \
Sed sit amet ligula a diam placerat imperdiet. Fusce in quam vehicula odio pharetra maximus. Aliquam eget nunc sollicitudin, \
fermentum ipsum bibendum, convallis nisl. In nec eros turpis. Donec et ultricies quam. Etiam ipsum erat, consequat et \
bibendum id, eleifend sit amet est. Curabitur sit amet tincidunt ante, at congue orci.

Press [space] to continue.
"""

componentSettings = dict(
    visual_components = dict(
        text = dict(
            name = "text",
            type = "TextStim",
            spec = dict(
                name = "text",
                color = "white",
                height = 0.03,
                text = text
            )
        )
    ),
    response = dict(
        keys = ["space"]
    )
)

data_handler = DataHandler("ScreenTest")
input_device = Keyboard()
window = Window(window_settings)

screen = Screen(window, input_device, data_handler, componentSettings)

screen.run()
