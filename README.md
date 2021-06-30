# psychopy-conflict-task
A generic Conflict Task boilerplate made in PsychoPy

## Installation
**Prerequisite**

1. Python version 3.6 or higher
2. `virtualenv` (Optional)
3. `virtualenvwrapper` (Optional)
    * For Windows, use `virtualenvwrapper-win`

*Note:* As of 30.06.2021, the newest version of **PsychoPy** is written for Python version 3.6. If you are using Windows and Python version 3.7 or higher, there are certain packages that are not compatible and must be downloaded and installed manually for your version. The wheels for multiple python packages can be found [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

**Example:** This package was developed using Windows 10 64-bit and Python version 3.9 and we encountered errors with PyTables and PyWinhook. Therefore we include the wheels for these packages in the '/manual_requirements/' folder.

To install these you do: `pip install [package file]`

In our case we do:

```sh
pip install manual-requirements/pyWinhook-1.6.2-cp39-cp39-win_amd64.whl
pip install manual-requirements/tables-3.6.1-cp39-cp39-win_amd64.whl
```

**Recommended Install**

1. `pip install requirements.txt`

**Installing using a newer version of PsychoPy**

1. `pip install psychopy`