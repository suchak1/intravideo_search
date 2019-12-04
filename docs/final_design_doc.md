## IntraVideo Search
## Final Design Document

### Functionality
#### Proposed and implemented functionality:
- Taking in video input
- Saving clips from video that match given search terms using machine learning API
- Allowing users to select clips by confidence, polling rate, and anti
- Displaying clips with timestamps (timestamps are in the title of each saved clip)

#### Proposed, but not implemented functionality:
- We decided to simply save clips to disk, so we could focus on other functionality instead of letting user view or choose clips first in the GUI itself.
- We eliminated the need for error messages using a slider that forced the user to select from the set of valid input values. Therefore, the only valid inputs are ones that are available on the GUI. We test for invalid inputs too in `verify_settings` in view.py

#### Implemented, but not proposed functionality:
- The application can take YouTube links and download them + automatically add them to the Job pipeline for classification.
- Multiprocessing allows for concurrency within each of these steps: pulling frames, classifying them, and saving clips.
- Image captioning allows users to see the ML model's output for each clip.

### Who Did What:

#### *Mahmoud:*
GUI `get_settings` and `set_settings`, work with *Jeremy*, *AK*.
Added a start and cancel button to the GUI and added the functions to connect the frontend and the backend.
Introduced functions to capture any errors from the code and display them to the user.
Worked with *Jeremy* to optimize the GUI and its features and worked with *AK* to make `set_settings` produce robust error messages for the user.

#### *Rachel:*
`Job` constructor and `get_frames`, work with *Ralph*.
Implemented an option for the user to input a URL link to a YouTube video instead of uploading a video file.
Discussed with *Krish* on handling updating `get_frames()` tests.
Wrote `README` for interation 1 and interation 2.
Wrote user guide with *Krish*.

#### *Jeremy:*
GUI constructor and render, work with *Mahmoud*, *AK*.
Fixed errors and optimized the GUI in order to improve testing and user experience, e.g. removing add/clear buttons (implementing comma separated search terms instead). 
Reworked GUI tests to work in compliance with Travis build. 
Made GUI look as good as possible with current knowledge of the GUI package.
Added the `Seer` class sentence caption to the GUI after the process has been started.
Worked with *Mahmoud* to round out the frontend development and David and *Krish* to connect the frontend with the backend.

#### *David:*
Implemented `interpret_results()` which takes the normalized scores and timestamps of sampled frames and outputs the time-ranges which constitute the positive search results (subclips of the original video) with *Krish* and *Ralph*.
Implemented `make_clips()` which takes a list of tuples of times, cuts subclips out from the original video, and saves them to a specified directory with *Ralph*.
Implemented the `Seer class` which is wrapper for the pytorch RNN based model which produces descriptive captions for the subclips created through the search.
Implemented the error-handling for the YouTube downloading feature, so that now if the download fails for network or encoding reasons the user is notified through the GUI and encouraged to try a different link.
Did general bug hunting / fixing throughout and was an active member during meetings where we came up with ideas of how to implement the program.

#### *AK:*
`Job` `start_job` and `kill_job`, work with *Jeremy*, *Mahmoud*.
Wrote and aggregated error messages in the GUI so the program could directly tell users what parts of their input were entered or processed incorrectly.
Worked with *Mahmoud* to make `set_settings` produce robust error messages for user.
Wrote final design document.

#### *Michael:*
`Worker` constructor, reviewed majority of PRs.
Created feature in GUI to select an output clip and provide a caption, description, of what is happening in the clip.

#### *Krish:*
- Worker `classify_img` and last min various bug fixes, work with *Ralph*, *David*.
Takes image and outputs classification labels and probabilities.
- Implemented `get_related_words` for semantic similarity. Gets related words, so user does not have to search for exact classification label to receive matching clip. For example, search `spring` will get videos of `fountain` as well.
- Updated `get_frames` implementation and testing from Iteration 1. Our previous implementation wrote `opencv` images to disk and then converted them to PIL images, cleaning up the image files on disk afterwards. Now, we convert the `opencv` images straight to PIL images and store them in memory directly, without writing to the user’s disk.
    - Discussed with Rachel on handling updating `get_frames` tests.

- Entirety of multiprocessing. Now `get_frames` pulls frames in parallel, `classify_img` classifies images in parallel, and `save_clips` saves clips in parallel as each of the elements of each operation is independent of one another.

- GUI refresh - second version of GUI with theme and responsiveness during Job. Used pygubu Tkinter GUI designer to make it, and loaded the Job in a separate process, so user can still interact with GUI while Job occurs (including cancelling the Job) - before this, GUI would freeze until clips were saved when user clicked Start.

- Blackbox utility (`src/analyze.py`). Allows user to see if search terms are "model-safe" before using GUI and processing/classifying video (not perfect solution, but workaround).
- Multiprocessing checkmark functionality alongside Mahmoud.
- Added pseudo-progress bar that loads until Job ends. Collects data on whether process has completed or not. Does not show actual numerical progress - main purpose is to show user that something is happening without user having to look at command line.

#### *Ralph:*
Job `classify_frames` and `save_clips`, work with *Rachel*, *Krish*, *David*  
Updated GUI by reorganizing the grid layout to be more intuitive, visually appealing, and easy to program, added toggling functionality to the Display settings button (now offering Hide settings when clicked), and made the displayed settings dynamically update when any constituent setting is changed (instead of only when Display settings is clicked). Worked alone on these changes, but collaborated with others (*Jeremy*, *Krish*, *David*) while hunting bugs and formulating details of backend implementation and frontend design.

### Checkpoint for source code
**v2.1** or latest by 4:00 PM https://github.com/suchak1/intravideo_search/releases
