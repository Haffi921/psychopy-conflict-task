from psychopy import visual

class Window(visual.Window):
    _window_setting = None

    def __init__(self, window_setting):
        self._window_setting = window_setting
        if self._window_setting["fullscreen"]:
            super().__init__(
                size = self._window_setting["size"],
                color = self._window_setting["color"],
                fullscr = True,
                screen = self._window_setting["screen"],
                monitor = self._window_setting["monitor"],
                winType = self._window_setting["winType"],
                useFBO = self._window_setting["useFBO"],
                units = self._window_setting["units"]
            )
        else:
            super().__init__(
                size = self._window_setting["size"],
                color = self._window_setting["color"],
                pos = self._window_setting["pos"],
                screen = self._window_setting["screen"],
                monitor = self._window_setting["monitor"],
                winType = self._window_setting["winType"],
                useFBO = self._window_setting["useFBO"],
                units = self._window_setting["units"]
            )