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

tetest_interpret_results_negative_score gives a list containing a result with a
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
