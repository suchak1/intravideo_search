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
