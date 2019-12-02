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

Input/Output Descriptions:
- test_get_frames()
    - get_frames() has no parameters (it is a method of the Job class and uses the Job attributes of video and poll as input)
    - The output of get_frames() is a list where each element is a tuple consisting of an Image of a frame and the timestamp in the video that the frame was taken.
    - The first test takes in the sample video 'SampleVideo_1280x720_1mb.mp4' from the sampleVideo directory and poll setting of 5 and returns a list of two Image and timestamp tuples. The first is the frame taken at 0 seconds and the second is the frame taken at 5 seconds.
    - The second test takes in the same sample video but with poll setting of 1 and returns a list of 6 Image/frame tuples: the frame at 0 seconds, the frame at 1 second, the frame at 2 seconds, the frame at 3 seconds, the frame at 4 seconds, and the frame at 5 seconds.
    - The last test takes in the sample video 'SampleVideoNature.mp4' from the sampleVideo directory and poll setting of 8 and returns a list of 4 Image/frame tuples: the frame at 0 seconds, the frame at 8 seconds, the frame at 16 seconds, and the frame at 24 seconds.
    - .jpg files of the expected images for all three tests can be found in the corresponding settings_poll_x folders within the sampleVideo folder.


![interpret_results]
interpret_results expects a list of tuples ((float)time, (float)score). The time 
should correspond to a frame of the video found at time seconds in. The score 
should be a number normalized to between 0 and 1. interpret_results also allows
for a "cutoff" parameter which determines the score necessary to be considered
a positive search result. Upon finding one or more positive results among the 
tuples in the given list, the function calculates the start and end times of
the relevant clips. The start time is computed by taking the midpoint in time
between a positive result, and the result before it. The end time is computed by 
taking the midpoint in time between the final positive result in a contiguous
sequence of positive results and the result after that. If either the first or
last positive result of the contiguous sequence of positive results is the very
first or last result in the given list, then the start/end time is the start/end
time of the video respectively, rather than a midpoint. Default cutoff is 0.5.
The return type is a list of tuples of start/end times.


test_interpret_results_null_input gives a Nonetype as the input list. An
exception should be raised.

test_interpret_results_negative_time gives a list containing a result with a 
negative time signature. An exception should be raised.

test_interpret_results_negative_score gives a list containing a result with a
negative score. An exception should be raised.

test_interpret_results_unnormalized_score gives a list containing a result with 
a score outside of the range of [0,1]. An exception should be raised.

test_interpret_results_duplicate_times gives a a list containing two results 
with identical time signatures. An exception should be raised.

test_interpret_results_negative_cutoff gives a valid list, but a negative 
cutoff value. An exception should be raised.

test_interpret_results_out_of_order gives an unordered list of results. An 
exception should be raised.


test_interpret_results_mid_clip gives a list of results contining a positive
result in the middle of the list. Namely, it gives: 
[(0.0, 0.1), (10.0, 0.6), (20.0, 0.3), (30.0, 0.2)]
This should return
[(5.0, 15.0)].

test_interpret_results_spanning_clip gives a list of results containing a 
contiguous series of positive results in the middle. Namely, it gves:
[(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.01)] 
This should return 
[(5.0, 25.0)].

test_interpret_results_multiple_seperate_clips gives a list of results 
containing multiple non-contiguous positive results. Namely, it gives:
[(0.0, 0.2),(10.0, 0.6),(20.0, 0.5),(30.0, 0.1),(40.0, 0.7),(50.0, 0.8),(60.0, 0.01)]
This should return
[(5.0, 25.0), (35.0, 55.0)]


test_interpret_results_from_start gives a list of results containing a positive
result at the start of the list. Namely, it gives:
[(1.0, 0.6), (10.0, 0.2), (20.0, 0.1), (30.0, 0.08)]
This should return
[(0.0, 5.5)]


test_interpret_results_from_end gives a list of results containing a positive
result at the end of the list. Namely, it gives:
[(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
This should return
[(25.0, 40.0)]

test_interpret_results_zero_cutoff gives a valid list of results with a cutoff
of zero. This should return the range of the whole video. Namely:
[(0.0, 40.0)]

test_interpret_results_cutoff_morethan_1 gives a valid list of results with a
cutoff more than 1. Since scores are notmalized to 1, this should return an
empty list.


![make_clip]
make_clip is designed to take in a single tuple of floats, signifying the start
and end time of the desired clip, in seconds, along with a filepath to the video file
which the clip is meant to be clipped from. The return type is a string, a 
filepath to the newly created clip. The destination filepath can be specified as
an argument.

For the tests, the input video used is:
"test/sampleVideo/SampleVideo_1280x720_1mb.mp4"


test_make_clip_negative_time gives a tuple with a negative time in it. Namely:
(-1.0, 30.0)
This should raise an exception.

test_make_clip_out_of_order gives a tuple where the start time is after the 
end time. Namely:
(10.0, 5.0)
This should raise an exception.

test_make_clip_null_input gives a Nonetype instead of a tuple.
This should raise an exception.

test_make_clip_zero_delta gives a tuple where the start time and the end time
are equal. Namely:
(2.0, 2.0)
This should raise an exception.

test_make_clip_invalid_vidpath gives a valid tuple, but a filepath into a 
directory that does not exist. Namely:
"this/doesntExist.mp4"
This should raise an exception.

test_make_clip_no_frames gives a tuple with an extremely small delta.
Namely:
(1.0, 1.0000001)
Since this produces no frames, this should return an empty string.

test_make_clip_full_video gives a tuple encompassing the entire video, and a 
destination filepath. Namely:
(0.0, 100000000000.0), and "test/sampleVideo/testFull.mp4"
This should return "test/sampleVideo/testFull.mp4" and testFull.mp4 should be
identical to the input video.

test_make_clip_from_mid gives a valid tuple marking a clip in the middle of the
sample video, and a destination path. Namely:
(1.0, 3.0), and "test/sampleVideo/testMid.mp4"
This should return "test/sampleVideo/testMid.mp4" and testMid.mp4 should be 
identical to the 1.0 through 3.0 seconds of the sample video.

test_make_clip_from_start gives a valid tuple marking a clip which begins at the
start of the sample video, and a destination path. Namely:
(0.0, 3.0), and "test/sampleVideo/testStart.mp4"
This should return "test/sampleVideo/testStart.mp4" and testStart.mp4 should be
identical to the first 3 seconds of the smaple video.

test_make_clip_from_end gives a valid tuple marking a clip which ends at the 
end of the sample video, and a destination path. Namely: 
(3.0, 1000000.0), and "test/sampleVideo/testEnd.mp4"
This should return "test/sampleVideo/testEnd.mp4" and testEnd.mp4 should be 
identical to the sample video staring 3 seconds in.

- test_set_settings()
    - set_settings(self, values, path) takes in two parameters: a dictionary of settings and a file path to the video. It will validate the settings and the validity of the path and return True if the settings are valid (as well as actually set the settings so the Job class can work) or False otherwise.
    - "values" is a dictionary path containing the following elements:
        - "conf": the confidence interval of acceptance of a frame classification. It must be a value between 0 and 1
        - "poll": the rate of how we pull frames to classify. It must be an integer value greater than 0
        - "anti": the amount of time in seconds where we do not accept a frame classification (giving us the bounds of the clip). It must be an integer value greater than 0
        - "runtime": the runtime of the video in seconds. Must be an integer greater than 0
        - "search": an array of search terms to use. It must be an array of strings
    - "path" is an OS path to the video to import. Python must be able to open the path.
    - If any of these conditions are false, then the default values will automatically be registered (the default values are: conf: 0.9, poll: 5, anti: 5, runtime: 1, search: [], path: ''. Not all of these are valid inputs, but this is intended to be the case to force the user to properly upload a video and specify search terms) and False will be returned.
    - In test_set_settings(), 24 different sets of settings with two paths (so 48 different test cases) are used. This is intended to test each separate element being invalid and testing whether the code breaks or not.
    - For example, set10 ({'conf': 0.9, 'poll': 5.2, 'anti': 5, 'runtime': 10, 'search': ['dog', 'pet']}) has an invalid parameter for "poll", so set_settings(set10, video_path) would return False
    
- test_get_settings()
    - get_settings() takes in no parameters and returns a dictionary containing the video path and the settings parameters.
    - If a previous call to set_settings() was successful, then get_settings() will return all of the parameters specified by set_settings() (since the settings were set properly). If this call to set_settings() was unsuccessful, then get_settings() will return the default settings and default video path. This would ensure that the user cannot initiate a Job without specifying the correct settings
    - In test_get_settings(), 24 different sets of settings with two paths (so 48 different test cases) are used. This is intended to test whether variations of incorrect settings will be considered in setting the default test cases.
    - For example, set 10 ({'conf': 0.9, 'poll': 5.2, 'anti': 5, 'runtime': 10, 'search': ['dog', 'pet']}) has an invalid parameter for "poll", so get_settings() would return the default settings.
    
- test_render()
    - render() takes in no parameters and returns 0 at the end to signify that the GUI has opened and closed. 
    - render() takes the current settings of the GUI object, specifically the contents of the 'values' dictionary described above as well as the video file path.
    - Although in the current GUI tests, the GUI should display the settings and video path that are current part of the GUI object, in practice, the GUI will only need to display the GUI settings.
    - The GUI allows the user to change the video path as well as the settings using the slider and the text box. 
    - test_render() also contains some invalid settings in order to make sure the GUI does not render these invalid settings.
    - test_render() currently has the render() function calls commented out in order to allow the tests to pass the travis build and pytest because it opens up a window and that will cause both to automatically fail. When actually implementing, these statements are not commented out.
    - Because the frontend has not yet connected to the backend, the Job parameter of the GUI is also commented out for now. Once connected, the GUI will be able to start a job. This will be implemented in iteration 2.
    - In test_render(), 12 total tests are used, varying the settings, the video path, and the job (not yet connected). Invalid settings are tested, even though these will be filtered out by the tests for set_settings(). Invalid video paths are tested for in test_model.py, so they are not included in test_render(). 
    - In practice the GUI will not have to render any invalid values, as the GUI only allows the user to change their settings and path to valid ones.

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
