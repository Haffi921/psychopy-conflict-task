import os
from sys import path

from psychopy import core, clock, gui, data, logging
from psychopy.hardware import keyboard
from psychopy import __version__

from conflict_task.devices import input_device
from conflict_task.devices import Window, InputDevice, DataHandler

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
    input_device: InputDevice = None
    data_handler: DataHandler = None

    # Trials
    trial = None
    subject_sequence = None

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
        if hasattr(input_device, experiment_settings["input_device"]):
            self.input_device = getattr(input_device, experiment_settings["input_device"])
        else:
            logging.fatal(f"No input device named {experiment_settings['input_device']}")
            core.quit()
        
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
    
    def previewStim(window_setting, stim_settings):
        win = Window(window_setting)
        stim = VisualComponent(win, stim_settings)
        inputDevice = keyboard.Keyboard()

        stim._turnAutoDrawOn()
        while True:
            if inputDevice.getKeys(["escape"]):
                core.quit()
            win.flip()