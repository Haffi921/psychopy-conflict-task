from pathlib import Path

from psychopy import __version__, core, data, gui


class DataHandler:
    filename: str = None
    subject_info: dict = None
    _data_handler: data.ExperimentHandler = None

    @classmethod
    def start_participant_data(cls, experiment_name: str, dlg_info: dict = {}, _save=True, _dlg=True):
        data_dir = Path().absolute() / "data"
        version = __version__
        date = data.getDateStr()

        dlg_info: dict = {"participant": "", "session": "001", **dlg_info}

        if _dlg:
            dlg = gui.DlgFromDict(
                dlg_info, sortKeys=False, title=experiment_name
            )

            if not dlg.OK:
                core.quit()

        cls.subject_info = {
            "experiment_name": experiment_name,
            **dlg_info,
            "psychopy_version": version,
            "date": date
        }

        file_name = f"{cls.subject_info['participant']}_{cls.subject_info['session']}_{experiment_name}_{cls.subject_info['date']}"

        cls.filename = str(data_dir / file_name)

        cls._data_handler = data.ExperimentHandler(
            name=experiment_name,
            version=version,
            saveWideText=_save,
            savePickle=_save,
            dataFileName=cls.filename,
        )

        cls.add_data_dict(cls.subject_info)
    
    @classmethod
    def __del__(cls):
        cls.finish_participant_data()

    @classmethod
    def get_participant_number(cls):
        return int(cls.subject_info['participant'])

    @classmethod
    def save_as_csv(cls):
        cls._data_handler.saveAsWideText(fileName=cls.filename + ".csv")

    @classmethod
    def save_as_psydat(cls):
        cls._data_handler.saveAsPickle(fileName=cls.filename)

    @classmethod
    def finish_participant_data(cls):
        cls.save_as_csv()
        cls.abort()

    @classmethod
    def abort(cls):
        cls._data_handler.abort()

    @classmethod
    def next_entry(cls):
        cls._data_handler.nextEntry()
        cls.add_data_dict(cls.subject_info)

    @classmethod
    def add_data(cls, key, value):
        cls._data_handler.addData(key, value)

    @classmethod
    def add_data_dict(cls, data_dict: dict):
        for key, value in data_dict.items():
            cls.add_data(str(key), str(value).encode("unicode_escape").decode())

    @classmethod
    def add_data_dict_and_next_entry(cls, data_dict: dict):
        cls.add_data_dict(data_dict)
        cls.next_entry()
