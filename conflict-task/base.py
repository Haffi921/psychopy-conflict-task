from subprocess import run
import psychopy


from psychopy import visual, core
from psychopy.hardware import keyboard

win = visual.Window(
    size=(1920, 1200), fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')

defaultKeyboard = keyboard.Keyboard()

running = True

while running:
    if defaultKeyboard.getKeys(["escape"]):
        running = False

win.close()
core.quit()