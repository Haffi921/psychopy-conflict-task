from psychopy import visual

DEFAULT_WINDOW_SETTINGS = dict(
    # Size of the window in pixels (x, y)
    size=(1920, 1080),
    # Color of background as [r, g, b] list or single value. Each gun can take values between -1.0 and 1.0
    color=[0, 0, 0],
    # Create a window in ‘full-screen’ mode. Better timing can be achieved in full-screen mode
    fullscr=True,
    # If not fullscreen, then position of the top-left corner of the window on the screen (x, y)
    pos=(0, 0),
    # Which monitor? 0 is primary monitor, 1 is secondary, etc.
    screen = 0,

    #---- Rest are less useful settings to tinker with, so it's not recommended ----#
    monitor = 'BasicMonitor',

    # If False, window will have no mouse, toolbar, etc.
    allowGUI = False,

    # Set the window type or back-end to use
    winType="pyglet",
    # Use framebuffer object
    useFBO=True,
    # Defines the default units of stimuli drawn in the window (can be overridden by each stimulus).
    # Values can be None, ‘height’ (of the window), ‘norm’ (normalised), ‘deg’, ‘cm’, ‘pix’
    units="height",
)


class Window(visual.Window):
    def __init__(self, window_settings={}):

        self.window_settings = DEFAULT_WINDOW_SETTINGS | window_settings

<<<<<<< HEAD:conflict_task/devices/window.py
        super().__init__(**self.window_settings)
=======
        super().__init__(**self.window_settings)

        self.mouseVisible = False
>>>>>>> 6b9a2396e22e38c6f390c7f3a6bc0f29837e7966:src/conflict_task/devices/window.py
