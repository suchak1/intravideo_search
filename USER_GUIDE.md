# **User Guide:** ***IntraVideo Search***
[![Build Status](https://travis-ci.org/suchak1/intravideo_search.png?branch=master)](https://travis-ci.org/suchak1/intravideo_search)
[![Linux](https://img.shields.io/badge/os-Linux-1f425f.svg)](https://ubuntu.com/download/desktop)
[![Python 3.7](https://img.shields.io/badge/python-3.7-red.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![version](https://img.shields.io/github/v/tag/suchak1/intravideo_search)](https://github.com/suchak1/intravideo_search/tags)
***
*IntraVideo Search* is a search engine for video that uses ML image classification to take an input video and search terms and produces relevant video clips (i.e. clips that match the search terms).

## Getting Started

### Prerequisites

<!---Obtain a free API key.--->
These are hard requirements, and the program will not work without these.
- [x] Python 3.7
- [x] Linux (tested on Ubuntu or Windows Subsystem for Linux (WSL))
    - [Get Ubuntu for Windows 10] (https://tutorials.ubuntu.com/tutorial/tutorial-ubuntu-on-windows#0)
    - [Get Windows Subsystem for Linux] (https://docs.microsoft.com/en-us/windows/wsl/install-win10)
- [x] an internet connection (for API calls and YouTube downloads)

### Installation
If all prerequisites are met, follow these instructions to install.

1. Clone the repository:
```
$ git clone https://github.com/suchak1/intravideo_search.git
```

2. Install the necessary packages by running the following command:
```
$ python -m pip install -r requirements.txt
```
   If there is a problem installing `torch`, use this command:
   ```
   $ python -m pip install torch===1.3.1 torchvision===0.4.2 -f https://download.pytorch.org/whl/torch_stable.html
   ```
   then install the rest of the requirements as necessary.

Troubleshooting:
  - If you encounter installation errors, try installing (and eventually running the program) within a virtual environment (using Conda, Python virtualenv, or something similar)

Note: Make sure you specify the right python version when you make these commands if you have multiple python installations, i.e. `python3`.


## Running and Using the Program
Run `$ python src/start.py` to begin. Then the following steps can be taken from within the GUI.

1. Select a video by:
   - entering a YouTube video URL and click `Add` to add the video to the pending Job. To clear the video from the Job, click `Clear`.
      *Note: While hypothetically you can enter any YouTube video you'd like, keep in mind that entering an extremely long video (e.g. baby shark 10 hour version) will likely take a long time to download and a long time to classify all the images. YouTube at your own risk.*
   - clicking `Browse` and choosing a local video on your hard drive.

   You will see your selected video on the right in the Settings box.

2. Enter a search term (or multiple search terms separated by commas — whitespace doesn't matter).

3. Adjust the settings by moving the sliders in the Settings box.
    - ***Confidence (%)***: Refers to the confidence score given by the ML classifier (i.e. how confident the classifier is that your searched term appears within a given image). The program will only return clips that have at least the confidence level given in the settings.

    A high confidence level will likely result in fewer false positives, but also fewer clips. A low confidence level will likely result in more false positives, but more clips.

    - ***Poll Rate (sec)***: Refers to the frequency with which the program will pull a frame to check for searched items (e.g. a poll rate of 5 seconds will check for any searched items every 5 seconds). The poll rate also determines the length of the resulting clips.

    A low poll rate will likely result in more precise clip lengths and classifications, but also longer run time. A high poll rate will likely result in less precise clip lengths and classifications, but also shorter run time.

4. To enable multiprocessing (CPU intensive concurrency), enable the multiprocessing checkmark. This will drastically speed up the Job but will also eat up CPU resources.

5. Press `Start Job` to start a Job with the specified settings and inputs (video and search terms). You can cancel at any time as the `Start Job` button will automatically become a `Cancel` button.

6. When the Job, the Log at the bottom of the window will output whether any relevant clips were found and how many. These clips will be saved in the source video's original filepath.

Extra:

7. Press `Choose Clip` to choose a video clip to caption. This action is available even while a Job is running.

![GUI](pics/gui_v2_working.PNG)
