## IntraVideo Search
## Specifications for Milestone 3.b

### (1) How to Compile
- To install all necessary packages, run:
    ```
    pip install -r requirements.txt
    ```
    - note: Python 3.7 is required

### (2) How to Run Code
- To start the GUI, run:
    ```
    python src/start.py
    ```

### (3) How to Run Unit Tests
- To run all tests, run 
    ```
    pytest -vv
    ```
    - `-vv` ensure verbose output
    - if there is a module import error, run `python -m pytest -vv`
- Note: to run a single test file, just append the test file path like so
    ```
    pytest test/test_controller.py -vv
    ```
    and to run a single function, add the `-k` flag and the function name:
    ```
    pytest test/test_controller.py -k "test_classify_img" -vv
    ```
    This might be necessary since functions like `classify_img` take a while because loading a ML model for the first time is expensive.


### (4) Acceptance tests
As we are unsure if the program works end to end with the frontend
interacting fully with the backend, our tests currently are those found in the
test_x.py files. There are several sample videos and images provided, however,
for these tests.

By running `python src/start.py`, you can start the GUI for yourself and try to add a video. Settings should update as you use the GUI.
![GUI](../pics/GUI.PNG)

We have also included a Jupyter notebook, so you can part of the backend dynamically.
Simply run `jupyter notebook` (make sure you have it installed, not a Python package) in the main directory and select `classify_img.ipynb` in your browser. Click Cell in the taskbar/menu and Run All. Now, note that the notebook successfully recognizes a goldfish with 99% confidence. Feel free to input/replace a URL of your choice to test object detection. ![classify_img](../pics/classify_img.PNG)


- test_set_settings()
    - set_settings(self, values, path) takes in two parameters: a dictionary of settings and a file path to the video. It will validate the settings and the validity of the path and return True if the settings are valid (as well as actually set the settings so the Job class can work) or False otherwise.
    - "values" is a dictionary path containing the following elements:
        - "conf": the confidence interval of acceptance of a frame classification. It must be a value between 0 and 1
        - "poll": the rate of how we pull frames to classify. It must be an integer value greater than 0
        - "anti": the amount of time in seconds where we do not accept a frame classification (giving us the bounds of the clip). It must be an integer value greater than 0
        - "runtime": the runtime of the video in seconds. Must be an integer greater than 0
        - "search": an array of search terms to use. It must be an array of strings
    - "path" is an OS path to the video to import. Pyhton must be able to open the path.
    - If any of these conditions are false, then the default values will automatically be registered (the default values are: conf: 0.9, poll: 5, anti: 5, runtime: 1, search: [], path: ''. Not all of these are valid inputs, but this is intended to be the case to force the user to properly upload a video and specify search terms) and False will be returned.
    - In test_set_settings(), 24 different sets of settings with two paths (so 48 different test cases) are used. This is intended to test each separate element being invalid and testing whether the code breaks or not.
    - For example, set10 ({'conf': 0.9, 'poll': 5.2, 'anti': 5, 'runtime': 10, 'search': ['dog', 'pet']}) has an invalid parameter for "poll", so set_settings(set10, video_path) would return False
    
- test_get_settings()
    - get_settings() takes in no parameters and returns a dictionary containing the video path and the settings parameters.
    - If a previous call to set_settings() was successful, then get_settings() will return all of the parameters specified by set_settings() (since the settings were set properly). If this call to set_settings() was unsuccessful, then get_settings() will return the default settings and default video path. This would ensure that the user cannot initiate a Job without specifying the correct settings
    - In test_get_settings(), 24 different sets of settings with two paths (so 48 different test cases) are used. This is intended to test whether variations of incorrect settings will be considered in setting the default test cases.
    - For example, set 10 ({'conf': 0.9, 'poll': 5.2, 'anti': 5, 'runtime': 10, 'search': ['dog', 'pet']}) has an invalid parameter for "poll", so get_settings() would return the default settings.
    

### (5) Text Description of Implementation
For the GUI and Input/Output:
We created a working GUI interface, that takes the video source input and
search terms and saves them to be accessible by the other API. The GUI will
also allow the user to change these settings, which will also be stored.

For the local data processing:
We have separated the video source file into individual frames.

For API interaction:
Our implementation sends the information to the ML model in the form of a single
picture. We only receive a very limited prediction of the most prevalent object
in the picture and a confidence score. In the next iteration, we will work on
accuracy, matching similar terms, and composing a sentence based on what is happening in the video.

Note:
The basic string processing and semantic similarity from the original plan for iteration 1 has been
moved to iteration 2.

### (6) Who Did What
- **Jeremy:** GUI constructor and render, work with Mahmoud, AK
- **Mahmoud:** GUI get_settings and set_settings, work with Jeremy, AK
- **AK:** GUI/Job start_job and kill_job, work with Jeremy, Mahmoud
- **Rachel:** Job constructor and get_frames, work with Ralph
- **Ralph:** Job classify_frames and save_clips, work with Rachel, Krish, David
- **David:** Job interpret_results and Worker make_clip, work with Krish and Ralph
for interpret_results, work with Ralph for make_clip
- **Krish:** Worker classify_img and last min various bug fixes, work with Ralph, David
- **Michael:** Worker constructor, reviewed majority of PRs

### (7) Design/Unit Test Changes
- **Krish:** comments in test_classify_img explain - mostly changed filenames and
replaced some test images because limitations of model trained to
identify only 1000 images
- **Rachel:** changed get_frames to return image/timestamp tuples and changed tests
to reflect this, also added more tests to get_frames per comments
from milestone 3a
- **David:** made comments preceding the make_clip tests indicating minor changes
in the way the ground-truth is generated
- **Mahmoud:** Added unit test for default GUI settings; video path changes
Note: other minor changes are noted in the comments in the test filenames
- **Jeremy:** Commented out the render function calls as this would not work with the travis build
and would not pass the pytest. 

### (8) Notes for TA
While unit tests pass, it is not entirely certain if the program works end to
end with the frontend interacting fully with the backend. This will be
reconciled in Iteration 2.
