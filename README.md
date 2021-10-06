# PsychoPy Conflict Task
A generic Conflict Task boilerplate made in PsychoPy


## Roadmap
- Add AudioComponents
- Add functionality to show non-trial screens (experiment info, etc)
- Add additional trial functions
    - Response feedback
    - Component disappearance after feedback
    - Possibly: Selective component display dependent on trial settings

## Installation
**Prerequisite**
1. Python version >=3.6, <=3.8
2. Install [Poetry](https://python-poetry.org/)
3. Run `poetry install` with additional `-D` flag for dev-dependancies
4. Run `poetry shell`

<br>

**Trouble using Python 3.9 or higher**

As of 06.10.2021, the newest version of **PsychoPy** is written for Python version 3.6. This project uses Python version 3.8.10, which also works. If you are using Windows and Python version 3.9 or higher, there are certain packages that are not compatible and must be downloaded and installed manually for your version. The wheels for multiple python packages can be found [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

**Example:** This package was developed using Windows 10 64-bit and Python version 3.9 and we encountered errors with PyTables and PyWinhook. Therefore we include the wheels for these packages in the '/manual_requirements/' folder.

To install these you do: `pip install [package file]`

In our case we do:

```sh
pip install manual-requirements/pyWinhook-1.6.2-cp39-cp39-win_amd64.whl
pip install manual-requirements/tables-3.6.1-cp39-cp39-win_amd64.whl
```