import os
from sys import path

from psychopy import core, clock, gui, data, logging
from psychopy.hardware import keyboard
from psychopy import __version__

from conflict_task.devices import Window

from .component import VisualComponent, ResponseComponent, BaseComponent
from .sequence import Trial

FRAMETOLERANCE = 0.001

class Experiment:
    # Experiment/Subject info
    name = None
    filename = None
    #subjectDlgInfo = None

    # Number of blocks and trials
    nr_blocks = 0
    nr_trials = 0

    # Devices
    window: Window = None
    input_device: keyboard.Keyboard = None

    # Trials
    trial = None
    subject_sequence = None

    # Output
    data_handler = None

    # Time handlers
    clock = clock.Clock()

    # Debug
    debug_data = None

    def __init__(self, name, subject_sequence, experiment_settings,
        subjectDlgInfo = {'participant': '', 'session': '001'},
        debug_data = False):
        
        self.name = name
        self.start_participant_data(subjectDlgInfo)

        self.nr_blocks = experiment_settings["blocks"]["number"]
        self.nr_trials = experiment_settings["blocks"]["trials"]["number"]

        self.window = Window(experiment_settings["window_settings"])
        self.input_device = experiment_settings["input_device"](clock=self.trial.clock)
        
        visualComponents = experiment_settings["blocks"]["trials"]["visualComponents"]
        response = experiment_settings["blocks"]["trials"]["response"]
        
        # TODO: Remove this
        self.trial = Trial(self.window, self.input_device, self.data_handler, visualComponents, response)
        self.subject_sequence = subject_sequence


        self.debug_data = debug_data
    
    def run(self):
        continue_experiment = True

        for block in range(self.nr_blocks):
            for trial in range(self.nr_trials):
                continue_experiment = self.trial.run(self.subject_sequence[block][trial], self)

                if not continue_experiment:
                    break
            if not continue_experiment:
                break
        
        self.finish_participant_data()
        self.window.flip()
        self.window.close()
        core.quit()

    def start_participant_data(self, subjectDlgInfo):
        thisDir = os.path.abspath(path[0])
        version = __version__
        date = data.getDateStr()
        
        dlg = gui.DlgFromDict(subjectDlgInfo, sortKeys=False, title=self.name)
        
        if not dlg.OK:
            core.quit()

        subjectDlgInfo["date"] = date
        subjectDlgInfo["psychopyVersion"] = version
        subjectDlgInfo["expName"] = self.name

        self.filename = thisDir + os.sep + "data" + os.sep + f"{subjectDlgInfo['participant']}_{self.name}_{subjectDlgInfo['date']}"

        self.data_handler = data.ExperimentHandler(name=self.name, version=version, extraInfo=subjectDlgInfo, saveWideText=True, dataFileName=self.filename)
    
    def finish_participant_data(self):
        self.data_handler.saveAsWideText(fileName=self.filename + ".csv")
        self.data_handler.abort()
    
    def previewStim(window_setting, stim_settings):
        win = Window(window_setting)
        stim = VisualComponent(win, stim_settings)
        inputDevice = keyboard.Keyboard()

        stim._turnAutoDrawOn()
        while True:
            if inputDevice.getKeys(["escape"]):
                core.quit()
            win.flip()