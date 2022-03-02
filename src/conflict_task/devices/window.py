from __future__ import annotations

from psychopy import clock, core, logging, visual

DEFAULT_WINDOW_SETTINGS = dict(
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
    # Anti-aliasing
    multiSample=True,
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
    def turnoff(cls):
        cls._settings = DEFAULT_WINDOW_SETTINGS
        cls._window.flip()
        cls._window.close()
        cls.started = False

    @classmethod
    def _error_if_window_not_started(cls):
        if not cls.started:
            logging.error(f"Remember to start window: 'Window.start()'")

    @classmethod
    def size(cls):
        return cls._window.size

    @classmethod
    def pix2norm_size(cls, pix: tuple[int, int]):
        if cls._window.useRetina:
            return (pix / cls._window.size) * 2.0
        else:
            return pix / cls._window.size

    @classmethod
    def pix2norm_pos(cls, pix: tuple[int, int]):
        return (cls.pix2norm_size(pix) * 2.0) - (1, 1)

    @classmethod
    def pix2height_size(cls, pix: tuple[int, int]):
        if cls._window.useRetina:
            return (pix / cls._window.size[1]) * 2.0
        else:
            return pix / cls._window.size[1]

    @classmethod
    def pt2norm_size(cls, pt: int):
        pix = pt * 4 / 3
        if cls._window.useRetina:
            return (pix / cls._window.size[1]) * 2.0
        else:
            return pix / cls._window.size[1] * 2.0

    @classmethod
    def get_actual_framerate(
        cls, nIdentical=10, nMaxFrames=100, nWarmUpFrames=10, threshold=1
    ):
        cls._error_if_window_not_started()
        return cls._window.getActualFrameRate(
            nIdentical=nIdentical,
            nMaxFrames=nMaxFrames,
            nWarmUpFrames=nWarmUpFrames,
            threshold=threshold,
        )

    @classmethod
    def get_future_flip_time(cls, target_time: float = 0, clock: clock = None) -> float:
        cls._error_if_window_not_started()
        return cls._window.getFutureFlipTime(targetTime=target_time, clock=clock)

    @classmethod
    def flip(cls, clear_buffer: bool = True):
        cls._error_if_window_not_started()
        cls._window.flip(clearBuffer=clear_buffer)

    @classmethod
    def quit(cls):
        if cls.started:
            cls._window.flip()
            cls._window.close()
        core.quit()
