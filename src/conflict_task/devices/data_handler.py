import os
from sys import path

from psychopy import __version__, core, data, gui


class DataHandler:
    def __init__(
        self,
        experiment_name: str,
        subject_info: dict = {},
    ):
        self.filename: str = None
        self.experiment_name: str = experiment_name
        self.participant_number: int = None
        self.subject_info: dict = {"participant": "", "session": "001", **subject_info}
        self._data_handler: data.ExperimentHandler = None

    def start_participant_data(self, _save=True, _dlg=True):
        this_dir = os.path.abspath(path[0])
        version = __version__
        date = data.getDateStr()

        if _dlg:
            dlg = gui.DlgFromDict(
                self.subject_info, sortKeys=False, title=self.experiment_name
            )

            if not dlg.OK:
                core.quit()

        self.participant_number = int(self.subject_info["participant"])

        self.subject_info["date"] = date
        self.subject_info["psychopyVersion"] = version
        self.subject_info["expName"] = self.experiment_name

        self.filename = (
            this_dir
            + os.sep
            + "data"
            + os.sep
            + f"{self.subject_info['participant']}_{self.subject_info['session']}_{self.experiment_name}_{self.subject_info['date']}"
        )

        self._data_handler = data.ExperimentHandler(
            name=self.experiment_name,
            version=version,
            extraInfo=self.subject_info,
            saveWideText=_save,
            savePickle=_save,
            dataFileName=self.filename,
        )
    
    def get_participant_number(self):
        return self.participant_number

    def save_as_csv(self):
        self._data_handler.saveAsWideText(fileName=self.filename + ".csv")

    def save_as_psydat(self):
        self._data_handler.saveAsPickle(fileName=self.filename)

    def finish_participant_data(self):
        self.save_as_csv()
        self.abort()

    def abort(self):
        self._data_handler.abort()

    def next_entry(self):
        self._data_handler.nextEntry()

    def add_data(self, key, value):
        self._data_handler.addData(key, value)

    def add_data_dict(self, data_dict: dict):
        for key, value in data_dict.items():
            self.add_data(str(key), str(value).encode("unicode_escape").decode())

    def add_data_dict_and_next_entry(self, data_dict: dict):
        self.add_data_dict(data_dict)
        self.next_entry()
