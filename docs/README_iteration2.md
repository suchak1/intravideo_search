## IntraVideo Search
## Specifications for Milestone 4.b

### (1) How to Compile
- To install all necessary packages, run:
    ```
    python -m pip install -r requirements.txt
    ```
    - Note: Python 3.7 and a Unix-based OS or Windows Subsystem for Linux (WSL) are required.
    - Troubleshooting: If you encounter the error *ERROR: Could not install packages due to an EnvironmentError*, try adding `sudo` to the command or installing in a fresh virtual environment.

    If there is a problem installing `torch`, try this command:

    ```
    python -m pip install torch===1.3.1 torchvision===0.4.2 -f https://download.pytorch.org/whl/torch_stable.html
    ```

    Then, install the rest of requirements as necessary.

### (2) How to Run Code
- To start the GUI, run:
    ```
    python src/start.py
    ```
    - Note: Use `python3` if multiple versions are installed on your system.
- Within the GUI, upload a video file, or a valid YouTube link, select settings, and enter search terms. Display your video path, settings, and search terms by clicking "Display Settings". Start the search process by clicking the "Start" button. Close the window by clicking the x in the top left corner or by clicking "Kill this Window".

### (3) Testing
- To run all tests, run:
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

### (4) Acceptance tests

***Note:*** Multiprocessing/parallelized functions do not currently work on Mac OS, only Linux and Windows Subsystem for Linux. This means the GUI will break after pressing start on Mac OS. Our workaround is simply to disable multiprocessing if we detect Mac OS, and use slow/non-parallel versions of our functions. In the meantime, the following works efficiently on Linux (although uses 100% CPU due to multiprocessing).
To speed up the processes but achieve less accurate results, increase the polling rate.

Here are 3 acceptance tests:

First, run `python src/start.py` to start GUI. Then, choose the test video in `test/COSTA_RICA.mp4` using the `Upload` button. Input each of the following scenarios, and click Start. The output should match the expected outputs below.

1. Test 1
    - **Input:**
        - *Confidence:* 30%
        - *Polling Rate:* 2 sec
        - *Anti:* 5 sec (default)
        - *Search Terms:* beach

    - **Output:**
        - 3 clips in `test/` folder all of the beach
2. Test 2
    - **Input:**
        - *Confidence:* 50%
        - *Polling Rate:* 2 sec
        - *Anti:* 5 sec (default)
        - *Search Terms:* fountain

    - **Output:**
        - 3 clips in `test/` 1st and 3rd are waterfalls, 2nd clip is beach
3. Test 3
    - **Input:**
        - *Confidence:* 80%
        - *Polling Rate:* 2 sec
        - *Anti:* 5 sec (default)
        - *Search Terms:* frog

    - **Output:**
        - 5 clips in `test/` folder first 2 are frogs, middle is komodo dragon, last 2 are snakes



### (5) Text Description of Implementation
- **For the GUI and Input/Output, and local data processing:** We have connected the frontend to the backend of our program. We have also updated the GUI to have a cleaner and easier-to-use interface and to improve user experience. Fundamental testing features like displaying the settings and path as well having a kill window button were improved and implemented. Also, the add and clear buttons were removed from the search bar and instead, whatever is in the search bar at the time of starting the processing will be the terms that are searched for. This allows the user to delete search terms after they have been typed in. The sentence captioning feature has been added to the GUI.
- **For API interaction and Post-API Data Processing:** We have implemented a semantic similarity (matching search terms with related words) to improve/bolster the relevancy of outputted clips. This was implemented in the `get_related_words()` function. The function `classify_img()` leverages this function, which uses a related words API to build a more inclusive classification dictionary which goes to classify_frames. This means a user should be able to search for more than merely the 1000 predefined TestNet classifications/categories. For example, a classification label “sports_car” now will match user search terms for “car,” “roadster,” “ferrari,” “corvette,” etc.
- **New Features:**
  1. We have implemented a feature that returns a sentence caption that describes what is occurring in each clip. This is implemented through the new Seer class. It is based on a pretrained pytorch model found in an open source github repository (https://github.com/yunjey/pytorch-tutorial/tree/master/). The Seer class makes modifications to some of this code and refactors it into a standalone class, rather than a script to be called from without. It uses a combination of CNN recurrent neural networks to predict sequences of words given an input image. The return type is a string of whitespace separated words which make up the caption.
  2. We have implemented a feature that gives the user an option to input a URL link to a YouTube video instead of uploading a video file. We implemented this using an open source library called Pytube originally created by Nick Ficano (https://github.com/nficano/pytube). However, we encountered a few bugs in using the currently available version of Pytube, and thus created a my_pytube directory that contains the original Pytube source code with our edits.
- As mentioned in the previous milestone README, we have not implemented a way to display clips in the GUI.

### (6) Who Did What
- **Mahmoud:**
    - Added a start and cancel button to the GUI and added the functions to connect the frontend and the backend.
    - Introduced functions to capture any errors from the code and display them to the user.
    - Worked with Jeremy to optimize the GUI and its features and worked with AK to make `set_settings()` produce robust error messages for the user.
- **Rachel:**
    - Implemented an option for the user to input a URL link to a YouTube video instead of uploading a video file.
    - Discussed with Krish on handling updating `get_frames()` tests.
- **Jeremy:**
    - Fixed errors and optimized the GUI in order to improve testing and user experience, e.g. removing add/clear buttons (implementing comma separated search terms instead). Has also made the GUI look as good as possible with current knowledge of the GUI package.
    - Added the Seer class sentence caption to the GUI after the process has been started.
    - Worked with Mahmoud to round out the frontend development and David and Krish to connect the frontend with the backend.
- **David:**
    - Implemented the Seer class. This is the captioning feature of the project (see New Features in Section (4) for more information).
- **AK:**
    - Wrote and aggregated error messages in the GUI so the program could directly tell users what parts of their input were entered or processed incorrectly.
    - Worked with Mahmoud to make `set_settings()` produce robust error messages for user.
- **Michael:**
    - Created feature in GUI to select an output clip and provide a caption, description, of what is happening in the clip.
- **Krish:**
    - Implemented `get_related_words()` for semantic similarity (see API/post-API Data Processing in Section (4) for more information).
    - Updated `get_frames()` implementation and testing from Iteration 1. Our previous implementation wrote opencv images to disk and then converted them to PIL images, cleaning up the image files on disk afterwards. Now, we convert the opencv images straight to PIL images and store them in memory directly, without writing to the user’s disk.
    - Discussed with Rachel on handling updating `get_frames()` tests.
- **Ralph:**
    - Updated GUI by reorganizing the grid layout to be more intuitive, visually appealing, and easy to program, added toggling functionality to the `Display settings` button (now offering `Hide settings` when clicked), and made the displayed settings dynamically update when any constituent setting is changed (instead of only when `Display settings` is clicked). Worked alone on these changes, but collaborated with others (Jeremy, Krish, David) while hunting bugs and formulating details of backend implementation and frontend design.

### (7) Design/Unit Test Changes
- **Rachel:** Changed `get_from_yt()` tests to check that program raises exception when given invalid youtube url.
- **David:** Added some checks to Seer_init tests to check for new attributes added in implementation.
- **AK:** Changed the output of `set_settings()` to a tuple where the first value was the original return value, i.e. changed all the tests to check to see if the first item of the returned tuple was True or False, not the whole tuple.
- **Krish:** For `test_get_frames()`, turned strict pixel equivalence test into a test making sure 95% of the pixels between 2 images have RGB values +/- 5 of each other. For `test_get_related_words()`, changed spaces in filenames and changed “waterfall” to “spring” for a single test because “waterfall” was not within the related words for the term “fountain.” All other tests cases were unchanged however, verifying the effectiveness of `get_related_words()`.

### (8) Notes for TA
- Our prototype works in a limited capacity, restricted only by the accuracy of the API and ML models. For example, when searching the sample nature video (test/sampleVideo/SampleVideoNature.mp4), the only labels found by the classifier are ``{'ant', 'nematode', 'goldfish', 'leafhopper', 'lacewing', 'vine_snake', 'green_snake', 'common_newt', 'green_mamba', 'snail', 'eft', 'cucumber', 'slug', 'lycaenid', 'bell_pepper', 'wine_bottle', 'spider_web', 'Granny_Smith'}``. The problem here is that a user would be unlikely to search the video for terms like "bell pepper" or "lacewing", and would receive no clips if the search terms were "water" or "leaf". We have several rough ideas to work around this, e.g. query parent child relationships directly through API or utilize semantic similarity functionality to fetch words in the imagenet categories. As is, our implementation does what we intended from our proposal, however we'd ideally like to use the time before Milestone 5 to explore these rough ideas and potentially improve the program for the presentation.


The following are additions left to complete before the Dec deadline.

***TODO:***

1. displaying captions for outputted clips - I believe this in progress by Michael or Jeremy?
2. silence console warnings and display status bar for at least `classify_frames` and maybe `get_frames`
    - Right now, everything runs one thread except for multiprocessing. We should spawn new thread for Job, so that GUI is still responsive after pressing start.
3. switch GUI from Tk to ttk and use modern theme - aesthetic change
4. parallelization / multiprocessing for `get_frames` - should be straightforward following the example of `classify_frames`
    - will give next best speed boost after `classify_frames`
