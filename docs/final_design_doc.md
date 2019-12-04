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
- We eliminated the need for error messages using a slider that forced the user to select from the set of valid input values. Therefore, the only valid inputs are ones that are available on the GUI. We test for invalid inputs too in `verify_settings()` in view.py

#### Implemented, but not proposed functionality:
- The application can take YouTube links and download them + automatically add them to the Job pipeline for classification.
- Multiprocessing allows for concurrency within each of these steps: pulling frames, classifying them, and saving clips.
- Image captioning allows users to see the ML model's output for each clip.

### Who Did What:

*Mahmoud:*

Added a start and cancel button to the GUI and added the functions to connect the frontend and the backend.

Introduced functions to capture any errors from the code and display them to the user.

Worked with Jeremy to optimize the GUI and its features and worked with AK to make set_settings() produce robust error messages for the user.

*Rachel:*

Implemented an option for the user to input a URL link to a YouTube video instead of uploading a video file.

Discussed with Krish on handling updating get_frames() tests.

*Jeremy:*

Fixed errors and optimized the GUI in order to improve testing and user experience, e.g. removing add/clear buttons (implementing comma separated search terms instead). Has also made the GUI look as good as possible with current knowledge of the GUI package.

Added the Seer class sentence caption to the GUI after the process has been started.

Worked with Mahmoud to round out the frontend development and David and Krish to connect the frontend with the backend.

*David:*

Implemented the Seer class. This is the captioning feature of the project (see New Features in Section (4) for more information).

*AK:*

Implemented start_job() and kill_job()

Wrote and aggregated error messages in the GUI so the program could directly tell users what parts of their input were entered or processed incorrectly.

Worked with Mahmoud to make set_settings() produce robust error messages for user.

*Michael:*

Created feature in GUI to select an output clip and provide a caption, description, of what is happening in the clip.

*Krish:*

Implemented get_related_words() for semantic similarity (see API/post-API Data Processing in Section (4) for more information).

Updated get_frames() implementation and testing from Iteration 1. Our previous implementation wrote opencv images to disk and then converted them to PIL images, cleaning up the image files on disk afterwards. Now, we convert the opencv images straight to PIL images and store them in memory directly, without writing to the user’s disk.

Discussed with Rachel on handling updating get_frames() tests.

*Ralph:*

Updated GUI by reorganizing the grid layout to be more intuitive, visually appealing, and easy to program, added toggling functionality to the Display settings button (now offering Hide settings when clicked), and made the displayed settings dynamically update when any constituent setting is changed (instead of only when Display settings is clicked). Worked alone on these changes, but collaborated with others (Jeremy, Krish, David) while hunting bugs and formulating details of backend implementation and frontend design.

### Checkpoint for source code
v2.1 or latest by 4:00 PM https://github.com/suchak1/intravideo_search/releases