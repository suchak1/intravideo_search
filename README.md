# ***IntraVideo*** **Search**
[![Build Status](https://travis-ci.org/suchak1/intravideo_search.png?branch=master)](https://travis-ci.org/suchak1/intravideo_search)
[![Linux](https://img.shields.io/badge/os-Linux-1f425f.svg)](https://ubuntu.com/download/desktop)
[![Python 3.7](https://img.shields.io/badge/python-3.7-red.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![version](https://img.shields.io/github/v/tag/suchak1/intravideo_search)](https://github.com/suchak1/intravideo_search/tags)
#### a project for CMSC 22001 -- Software Construction
***
*IntraVideo Search* is a search engine that takes a video source and search terms as inputs and produces short video clips as outputs. Using ML image classification APIs, we can search through a video and retrieve only the parts relevant to the user-specified search terms.

## Getting Started

### Prerequisites

<!---Obtain a free API key.--->
These are hard requirements, and the program will not work without these.
- Python 3.7
- Linux (tested on Ubuntu 1or Windows Subsystem for Linux (WSL)
- an internet connection (for related words API calls and YouTube downloads)

### Contributing

To get set up, please read the [Guide to Git](docs/GUIDE_TO_GIT.md).


### Installation

To install the necessary packages, simply run:
```
python -m pip install -r requirements.txt
```

If there is a problem installing `torch`, try this command:

```
python -m pip install torch===1.3.1 torchvision===0.4.2 -f https://download.pytorch.org/whl/torch_stable.html
```

Then, install the rest of requirements as necessary.

### New Packages

To remake the `requirements.txt` file, run:
```
pipreqs ./ --force
```

### Testing

- To run all tests, first make the test suite executable (bash file).
    ```
    chmod +x test_suite.sh
    ```
    Then, run
    ```
    PYTHON=python ./test_suite.sh
    ```
    - where `python` is your python 3 installation (might be `python3` if you have more than one installation)
- Note: to run a single test file, just append the test file path like so
    ```
    python -m pytest test/test_controller.py -vv
    ```
    and to run a single function, add the `-k` flag and the function name:
    ```
    python -m pytest test/test_controller.py -k "test_classify_img" -vv
    ```
    This might be necessary since functions like `classify_img` take a while because loading a ML model for the first time is expensive.

Note: Make sure you specify the right python version when you make these commands if you have multiple python installations, ie `python3`.

### Prettify

To maintain consistent code style, consider executing the command:

```
autopep8 -i -r ./
```

This will automatically update/rewrite all Python code in the entire repo to follow PEP8 style guidelines.

## Deployment


## Running the Program

By running `python src/start.py`, you can start the GUI for yourself and try to add a video. Settings should update as you use the GUI.

1. Enter a YT video and click `Add` to add the video to the pending Job. To clear the video from the job, press `Clear`. Or you can choose a local video on your hard drive with the `Browse` button.

2. Enter a search term (or list of search terms delimited by commas - whitespace doesn't matter).

3. Adjust the settings if necessary.
    - A high confidence level will likely result in less false positives but also less clips. A low confidence level will likely result in more false positives but also more clips.
    - A low poll rate with likely result in more precise clip lengths and classification but also longer Job run time. A high poll rate will likely result in less precise clip lengths and classifications but also shorter Job run time.

4. To enable multiprocessing (CPU intensive concurrency), enable the multiprocessing checkmark. This is an experimental feature that will drastically speed up the Job but also eat up CPU resources.

5. Press `Start Job` to start a Job with the specified settings and inputs (video and search terms). You can cancel at any time as the `Start` button will automatically become a `Cancel` button.

6. When the Job completes, the Log will output whether any relevant clips where found and how many. These clips will be saved in the source video's original filepath.

***Extra:***
7. Press `Choose Caption` to choose a video clip to caption. This action is available even while a Job is running.

## Result

![GUI](pics/gui_v2_working.PNG)

We have also included a Jupyter notebook, so you can part of the backend dynamically.
Simply run `jupyter notebook` (make sure you have it installed, not a Python package) in the main directory and select `classify_img.ipynb` in your browser. Click Cell in the taskbar/menu and Run All. Now, note that the notebook successfully recognizes a goldfish with 99% confidence. Feel free to input/replace a URL of your choice to test object detection. ![classify_img](pics/classify_img.PNG)

## Files

```docs/``` - markdown files for software dev

```pics/``` - any screenshots used in markdown files

```src/``` - source code for the project

- ```model.py``` - main driver


- ```view.py``` - GUI

- ```controller.py``` - workhorse

```utils/``` - various scripts to help in dev work

- ```update.py``` - updates all packages that `pip` considers "outdated"
- ```dev_dep.py``` - lists dev dependencies (packages that aren't explicitly used in source code but you believe the project needs) - this allows the `requirements.txt` to be complete when we remake it with `pipreqs`

```.travis.yml``` - build pipeline



## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md)
 file for details.

***

[![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<!---
<<[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)>>
--->
