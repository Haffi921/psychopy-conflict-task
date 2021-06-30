# PsychoPy Conflict Task
A generic Conflict Task boilerplate made in PsychoPy

## Installation
**Prerequisite**
1. Python version 3.6 or higher
2. `pip install virtualenv` (Optional)
3. `pip install virtualenvwrapper` (Optional)
    * For Windows, use `pip install virtualenvwrapper-win`

<br>

**For the best experience, we recommend using virtualenv**

In *cmd*, *powershell* or *terminal*, type:
1. `mkvirtualenv psychopy`
2. `workon psychopy`

*Note:* `psychopy` is an optional name for you virtual environment, you can choose a different name

<br>

**Trouble using Python 3.7 or higher**

As of 30.06.2021, the newest version of **PsychoPy** is written for Python version 3.6. If you are using Windows and Python version 3.7 or higher, there are certain packages that are not compatible and must be downloaded and installed manually for your version. The wheels for multiple python packages can be found [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

**Example:** This package was developed using Windows 10 64-bit and Python version 3.9 and we encountered errors with PyTables and PyWinhook. Therefore we include the wheels for these packages in the '/manual_requirements/' folder.

To install these you do: `pip install [package file]`

In our case we do:

```sh
pip install manual-requirements/pyWinhook-1.6.2-cp39-cp39-win_amd64.whl
pip install manual-requirements/tables-3.6.1-cp39-cp39-win_amd64.whl
```

<br>

**Recommended Install**
1. `pip install -r requirements.txt`

**Installing using a newer version of PsychoPy**
1. `pip install psychopy`