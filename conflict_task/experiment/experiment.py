import os
from sys import path

from psychopy import core, clock, gui, data, logging
from psychopy.hardware import keyboard
from psychopy import __version__

from conflict_task.devices import Window

from .component import VisualComponent, ResponseComponent, BaseComponent

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
    dataHandler = None

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
        
        visualComponents = experiment_settings["blocks"]["trials"]["visualComponents"]
        response = experiment_settings["blocks"]["trials"]["response"]
        
        self.trial = Trial(self.window, visualComponents, response)
        self.subject_sequence = subject_sequence

        self.input_device = experiment_settings["input_device"](clock=self.trial.clock)

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

        self.dataHandler = data.ExperimentHandler(name=self.name, version=version, extraInfo=subjectDlgInfo, saveWideText=True, dataFileName=self.filename)
    
    def finish_participant_data(self):
        self.dataHandler.saveAsWideText(fileName=self.filename + ".csv")
        self.dataHandler.abort()
    
    def previewStim(window_setting, stim_settings):
        win = Window(window_setting)
        stim = VisualComponent(win, stim_settings)
        inputDevice = keyboard.Keyboard()

        stim.turnAutoDrawOn()
        while True:
            if inputDevice.getKeys(["escape"]):
                core.quit()
            win.flip()


class Trial:
    # TODO: Add AudioComponents, etc.
    visualComponents = []
    
    # Main conflict-task components
    response = None

    clock = clock.Clock()

    def __init__(self, window, visualComponents, response):
        for component in visualComponents:
            visualComponent = VisualComponent(window, component)
            
            self.visualComponents.append(visualComponent)
                
        self.response = ResponseComponent(response)

    def get_all_components(self) -> list[BaseComponent]:
        return [*self.visualComponents, self.response]

    def refresh(self):
        for component in self.get_all_components():
            component.refresh()
    
    def run(self, trial_values: dict, experiment: Experiment):
        self.refresh()

        for component in self.get_all_components():
            component.prepare(trial_values)

        for key, value in trial_values.items():
            experiment.dataHandler.addData(key, r"{}".format(value))

        running = True
        self.clock.reset(-experiment.window.getFutureFlipTime(clock="now"))
        
        while running:
            if experiment.input_device.getKeys(["escape"]):
                return False
            
            time = self.clock.getTime()
            thisFlip = experiment.window.getFutureFlipTime(clock=self.clock)
            thisFlipGlobal = experiment.window.getFutureFlipTime(clock=None)

            running = False

            for component in self.get_all_components():
                if component.not_started():
                    if thisFlip >= component.start_time - FRAMETOLERANCE:
                        component.start(time, thisFlipGlobal)
                elif component.started():
                    if thisFlip >= component.stop_time - FRAMETOLERANCE:
                        if experiment.debug_data:
                            component.stop(time, thisFlipGlobal, experiment.dataHandler)
                        else:
                            component.stop(time, thisFlipGlobal)
                
                if not component.finished():
                    running = True

            self.response.check(experiment.input_device, experiment.dataHandler)
            
            experiment.window.flip()
        
        experiment.dataHandler.nextEntry()
        
        return True