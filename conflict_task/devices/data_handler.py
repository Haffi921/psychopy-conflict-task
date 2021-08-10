import os
from sys import path

from psychopy import __version__

from psychopy import data, gui, core
from psychopy.logging import exp

class DataHandler:
    filename: str
    _data_handler: data.ExperimentHandler

    def __init__(self, experiment_name, subjectDlgInfo  = {'participant': '', 'session': '001'}):
        self.start_participant_data(experiment_name, subjectDlgInfo)

    def start_participant_data(self, experiment_name, subjectDlgInfo):
        thisDir = os.path.abspath(path[0])
        version = __version__
        date = data.getDateStr()
        
        dlg = gui.DlgFromDict(subjectDlgInfo, sortKeys=False, title=experiment_name)
        
        if not dlg.OK:
            core.quit()

        subjectDlgInfo["date"] = date
        subjectDlgInfo["psychopyVersion"] = version
        subjectDlgInfo["expName"] = experiment_name

        self.filename = thisDir + os.sep + "data" + os.sep + f"{subjectDlgInfo['participant']}_{experiment_name}_{subjectDlgInfo['date']}"

        self._data_handler = data.ExperimentHandler(name=experiment_name, version=version, extraInfo=subjectDlgInfo, saveWideText=True, dataFileName=self.filename)
    
    def finish_participant_data(self):
        self._data_handler.saveAsWideText(fileName=self.filename + ".csv")
        self._data_handler.abort()

    def abort(self):
        self._data_handler.abort()
    
    def add_data(self, key, value):
        self._data_handler.addData(key, value)
    
    def add_data_dict(self, dict: dict):
        for key, value in dict.items():
            self.add_data(str(key), str(value).encode("unicode_escape").decode())
    
    def next_entry(self):
        self._data_handler.nextEntry()