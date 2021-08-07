import os
from sys import path

from conflict_task.devices import Window, Keyboard, DataHandler
from conflict_task.experiment.sequence import Screen

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
window = Window()

screen = Screen(window, input_device, data_handler, componentSettings)

screen.run()
