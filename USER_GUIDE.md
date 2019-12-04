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
- [x] [Anaconda (Python 3.7)](https://www.anaconda.com/distribution/)
- [x] [Linux (Ubuntu 18.04)(https://ubuntu.com/download/desktop)]
- [x] an internet connection (for API calls and YouTube downloads)

Click the links above to download and install the software. If you are having trouble or would rather not, please take advantage of CSIL's Linux room. Those computers already have Ubuntu and Anaconda installed. If you are not sure whether Anaconda is installed, please ask CSIL staff for help in confirming. You can even ask them for help in making a new virtual environment (which is described in the next step).

### Installation
If all prerequisites are met, follow these instructions to clone the repo and install the necessary Python packages. From this point on, we will assume `python` is the command for your Anaconda Python 3.7 distribution.

1. Clone the repository:
```
$ git clone https://github.com/suchak1/intravideo_search.git
```

2. Navigate into the main directory (`intravideo_search/`):
```
$ cd intravideo_search
```

3. Create a new (fresh) Python 3.7 virtual environment (called `intra` in this case) for Anaconda:
```
$ conda create -n intra python=3.7
```

4. Activate the new environment:
```
$ conda activate intra
```

    To make sure the environment switched to `intra`, you can do `conda env list` and make sure the star is on the same row as `intra`. If not close bash, and try Step 4 again.

6. Confirm that running `python -V` yields Python 3.7. If not, make sure you specified the right Python version in Step 3 and have Anaconda for Python 3.7.

5. Install the necessary packages by running the following command:
```
$ pip install -r requirements.txt
```

    If the installation hangs for more than 10 min, cancel the command (Ctrl + C) and try again or ask staff at CSIL for help installing packages if you are at Crerar.

   If there is an error installing `torch` specifically, use this command:
   ```
   $ pip install torch===1.3.1 torchvision===0.4.2 -f https://download.pytorch.org/whl/torch_stable.html
   ```
   then install the rest of the requirements as necessary.



Note: Make sure you specify the right python version when you make these commands if you have multiple python installations, i.e. check to make sure `python -V` yields Python 3.7 otherwise your relevant command may be `python3`.


## Running and Using the Program
(Make sure you run the program and any utilities in the main dir (`intravideo_search/`).

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

***Extra:***

7. Press `Choose Clip` to choose a video clip to caption. This action is available even while a Job is running.

![GUI](pics/gui_v2_working.PNG)
