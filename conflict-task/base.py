from psychopy import visual, core

win = visual.Window(fullscr=True)
msg = visual.TextStim(win, text="Hello, world!")

msg.draw()
win.flip()
core.wait(3)
win.close()