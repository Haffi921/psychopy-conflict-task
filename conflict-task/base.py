from subprocess import run
import psychopy


from psychopy import visual, core
from psychopy import clock
from psychopy.constants import FINISHED, NOT_STARTED, STARTED
from psychopy.hardware import keyboard

win = visual.Window(
    size=(1920, 1200), fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')

defaultKeyboard = keyboard.Keyboard()

# Stims
fixation_cross = visual.ShapeStim(win, lineColor=None, fillColor="white", vertices="cross", size=0.05, name="fixation_cross")
fixation_cross.tStart = 0.0
fixation_cross.tDuration = 1.0

distractor = visual.TextStim(win, text="Down\nDown\nDown", color="white", height=0.05, name="distractor")
distractor.tStart = 1.0
distractor.tDuration = 0.133

target = visual.TextStim(win, text="Up", color="white", height=0.05, name="target")
target.tStart = 1.166
target.tDuration = 0.133

stims = [fixation_cross, distractor, target]
for stim in stims:    
    stim.status = NOT_STARTED
    stim.tStarted = None
    stim.tStartedRefresh = None
    stim.tStopped = None
    stim.tStoppedRefresh = None

# Trials
nr_trials = 5

# Clocks and times
globalClock = clock.Clock()
trialClock = clock.Clock()
_frameTolerance = 0.001

running_experiment = True

# TODO: Set up response

for current_trail in range(nr_trials):
    t = 0
    _timeToNextFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToNextFrame)

    running_trial = True

    for stim in stims:    
        stim.status = NOT_STARTED
        stim.tStarted = None
        stim.tStartedRefresh = None
        stim.tStopped = None
        stim.tStoppedRefresh = None

    while running_trial:
        if defaultKeyboard.getKeys(["escape"]):
            running_experiment = False
            break

        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)

        running_trial = False

        for stim in stims:
            if stim.status == NOT_STARTED:
                if tThisFlip >= stim.tStart - _frameTolerance:
                    stim.tStarted = t
                    stim.tStartedRefresh = tThisFlipGlobal
                    stim.setAutoDraw(True)
                    stim.status = STARTED
            elif stim.status == STARTED:
                if tThisFlip > stim.tStart + stim.tDuration - _frameTolerance:
                    stim.tStopped = t
                    stim.tStoppedRefresh = tThisFlipGlobal
                    stim.setAutoDraw(False)
                    stim.status = FINISHED
            
            if stim.status != FINISHED:
                running_trial = True
        
        win.flip()

    if running_experiment == False:
        break

win.close()
core.quit()