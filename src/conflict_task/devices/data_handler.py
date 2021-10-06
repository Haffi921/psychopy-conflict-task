import os
from sys import path

from psychopy import __version__, core, data, gui


class DataHandler:
    def __init__(
        self,
        experiment_name: str,
        subject_info: dict = {"participant": "", "session": "001"},
    ):
        self.filename: str = None
        self.experiment_name: str = experiment_name
        self.subject_info: dict = subject_info
        self._data_handler: data.ExperimentHandler = None

    def start_participant_data(self):
        thisDir = os.path.abspath(path[0])
        version = __version__
        date = data.getDateStr()

        dlg = gui.DlgFromDict(
            self.subject_info, sortKeys=False, title=self.experiment_name
        )

        if not dlg.OK:
            core.quit()

        self.subject_info["date"] = date
        self.subject_info["psychopyVersion"] = version
        self.subject_info["expName"] = self.experiment_name

        self.filename = (
            thisDir
            + os.sep
            + "data"
            + os.sep
            + f"{self.subject_info['participant']}_{self.experiment_name}_{self.subject_info['date']}"
        )

        self._data_handler = data.ExperimentHandler(
            name=self.experiment_name,
            version=version,
            extraInfo=self.subject_info,
            saveWideText=True,
            dataFileName=self.filename,
        )

    def finish_participant_data(self):
        self._data_handler.saveAsWideText(fileName=self.filename + ".csv")
        self._data_handler.abort()

    def abort(self):
        self._data_handler.abort()

    def next_entry(self):
        self._data_handler.nextEntry()

    def add_data(self, key, value):
        self._data_handler.addData(key, value)

    def add_data_dict(self, dict: dict):
        for key, value in dict.items():
            self.add_data(str(key), str(value).encode("unicode_escape").decode())

    def add_data_dict_and_next_entry(self, dict: dict):
        self.add_data_dict(dict)
        self.next_entry()
