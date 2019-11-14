IntraVideo Search
Specifications for Milestone 3.b

(1) How to Compile
- run "pip install -r requirements.txt" to install all necessary packages
- note: Python 3.7 is required

(2) How to Run Code
- run "python src/view.py" to run the GUI

(3) How to Run Unit Tests
- to run all tests, run "pytest"
- if there is a module import error run "python -m pytest"

(4) Acceptance tests
As we are unsure if if the program works end to end with the frontend
interacting fully with the backend, our tests currently are those found in the
test_x.py files. There are several sample videos and images provided, however,
for these tests.

(5) Text Description of Implementation
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
accuracy, matching similar terms, and composing a sentence based on whats
happening in the video

Note:
The basic string processing from the original plan for iteration 1 has been
moved to iteration 2.

(6) Who Did What
Jeremy: GUI constructor and render, work with Mahmoud, AK
Mahmoud: GUI get_settings and set_settings, work with Jeremy, AK
AK: GUI/Job start_job and kill_job, work with Jeremy, Mahmoud
Rachel: Job constructor and get_frames, work with Ralph
Ralph: Job classify_frames, work with Rachel, Krish, David
David: Job interpret_results and Worker make_clip, work with Krish and Ralph
for interpret_results, work with Ralph for make_clip
Krish: Worker classify_img, work with Ralph, David
Michael: Worker constructor, reviewed majority of PRs

(7) Design/Unit Test Changes
Krish: commented in changes to test_classify_img - mostly changed filenames
and commented out some test images because limitations of model trained to
identify only 1000 images
Rachel: changed get_frames to return image/timestamp tuples and changed tests
to reflect this, also added more tests to get_frames per comments
from milestone 3a
David: made comments preceding the make_clip tests indicating minor changes
in the way the ground-truth is generated
Mahmoud: Added unit test for default GUI settings; video path changes
Note: other minor changes are noted in the comments in the test filenames

(8) Notes for TA
While unit tests pass, it is not entirely certain if the program works end to
end with the frontend interacting fully with the backend. This will be
reconciled in Iteration 2.
