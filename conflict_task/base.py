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

distrator_text = "Down\nDown\nDown"
target_text = "Up"
correct_answer = "j"

# Stims
fixation_cross = visual.ShapeStim(win, lineColor=None, fillColor="white", vertices="cross", size=0.05, name="fixation_cross")
fixation_cross.tStart = 0.0
fixation_cross.tDuration = 1.0
fixation_cross.drawable = True

distractor = visual.TextStim(win, text=distrator_text, color="white", height=0.05, name="distractor")
distractor.tStart = 1.0
distractor.tDuration = 0.133
distractor.drawable = True

target = visual.TextStim(win, text=target_text, color="white", height=0.05, name="target")
target.tStart = 1.166
target.tDuration = 0.133
target.drawable = True

from types import SimpleNamespace
response = SimpleNamespace()
response.keys = ['a', 'd', 'j', 'k']
response.tStart = 1.3
response.tStop = 3.0
response.drawable = False

components = [fixation_cross, distractor, target, response]

# Trials
nr_trials = 5

# Clocks and times
globalClock = clock.Clock()
trialClock = clock.Clock()
_frameTolerance = 0.001

running_experiment = True

# TODO: Set up data logging

for current_trail in range(nr_trials):
    t = 0
    _timeToNextFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToNextFrame)

    running_trial = True

    for component in components:    
        component.status = NOT_STARTED
        component.tStarted = None
        component.tStartedRefresh = None
        component.tStopped = None
        component.tStoppedRefresh = None
        
        if hasattr(component, "tDuration"):
            component.tStop = component.tStart + component.tDuration
    
    response.made = False
    response.key = None
    response.rt = None
    response.correct = None

    while running_trial:
        if defaultKeyboard.getKeys(["escape"]):
            core.quit()

        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)

        running_trial = False

        for component in components:
            if component.status == NOT_STARTED:
                if tThisFlip >= component.tStart - _frameTolerance:
                    component.tStarted = t
                    component.tStartedRefresh = tThisFlipGlobal
                    component.status = STARTED
                    if component.drawable == True:
                        component.setAutoDraw(True)
            elif component.status == STARTED:
                if tThisFlip > component.tStop - _frameTolerance:
                    component.tStopped = t
                    component.tStoppedRefresh = tThisFlipGlobal
                    component.status = FINISHED
                    if component.drawable == True:
                        component.setAutoDraw(False)
            
            if component.status != FINISHED:
                running_trial = True
            
        if response.status == STARTED and not response.made:
            keyPressed = [(key.name, key.rt) for key in defaultKeyboard.getKeys(keyList = response.keys)]
            if len(keyPressed):
                response.key, response.rt = keyPressed[-1]
                response.made = True
                if response.key == correct_answer:
                    response.correct = 1
                else:
                    response.correct = 0

        win.flip()

win.close()
core.quit()