from psychopy import clock, core, logging, visual

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
    screen=0,
    # ---- Rest are less useful settings to tinker with, so it's not recommended ----#
    monitor="BasicMonitor",
    # If False, window will have no mouse, toolbar, etc.
    allowGUI=False,
    # Set the window type or back-end to use
    winType="pyglet",
    # Use framebuffer object
    useFBO=True,
    # Defines the default units of stimuli drawn in the window (can be overridden by each stimulus).
    # Values can be None, ‘height’ (of the window), ‘norm’ (normalised), ‘deg’, ‘cm’, ‘pix’
    units="pix",
)

"""
class Window(visual.Window):
    def __init__(self, window_settings={}):

        self.window_settings = {**DEFAULT_WINDOW_SETTINGS, **window_settings}

        super().__init__(**self.window_settings)

        self.mouseVisible = self.window_settings["allowGUI"]
"""


class Window:
    _window: visual.Window = None
    _settings: dict = DEFAULT_WINDOW_SETTINGS
    started: bool = False

    @classmethod
    def settings(cls, window_settings={}):
        cls._settings = {**DEFAULT_WINDOW_SETTINGS, **window_settings}

    @classmethod
    def start(cls, window_settings=None):
        if not cls.started:
            if window_settings:
                cls.settings(window_settings)

            cls._window = visual.Window(**cls._settings)

            cls._window.mouseVisible = cls._settings["allowGUI"]

            cls.started = True
        else:
            logging.warning(
                "Window already started. 'Window.start' is called more than once."
            )

    @classmethod
    def error_if_window_not_started(cls):
        if not cls.started:
            logging.error(f"Remember to start window: 'Window.start()'")

    @classmethod
    def get_future_flip_time(cls, target_time: float = 0, clock: clock = None) -> float:
        cls.error_if_window_not_started()
        return cls._window.getFutureFlipTime(targetTime=target_time, clock=clock)

    @classmethod
    def flip(cls, clear_buffer: bool = True):
        cls.error_if_window_not_started()
        cls._window.flip(clearBuffer=clear_buffer)

    @classmethod
    def quit(cls):
        if cls.started:
            cls._window.flip()
            cls._window.close()
        core.quit()

    @classmethod
    def __del__(cls):
        cls.quit()
