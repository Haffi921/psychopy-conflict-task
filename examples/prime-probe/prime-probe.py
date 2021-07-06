from psychopy import core, clock

from conflict_task.window import Window
from settings.device_settings import *


win = Window(window_settings)

# Clocks and times
globalClock = clock.Clock()
trialClock = clock.Clock()
_frameTolerance = 0.001

win.flip()

core.wait(2)

win.close()
core.quit()