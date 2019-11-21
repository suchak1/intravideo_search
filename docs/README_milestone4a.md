## IntraVideo Search
## Specifications for Milestone 4.a

### (1) Plan for Implementation 2
- For the GUI and Input/Output, and local data processing:
    We are focusing on making sure that the frontend connects to the backend. We will also be updating the GUI to have a cleaner and easier-to-use interface. Previously, we intended to include a way for the clips to be displayed in a helpful way and to implement an option for the user to download the individual clips from the GUI. We will not be doing this anymore because after Iteration 1, we decided that it is not reasonable to display a potentially large number of clips on screen, so the implementation for Iteration 2 will simply save clips without giving the user any other option.
- For API interaction and Post-API Data Processing:
    We are planning to implement a semantic similarity graph that will allow users to set a recursion depth for how many “similar” results semantically to the search term they want to search for. This feature is described in detail in the previously submitted design document.
- New Features:
    We will also be implementing two new features. First, we will implement a new feature that returns a sentence caption that describes what is occurring in each clip. Second, we will implement an option for the user to input a URL link to a YouTube video instead of uploading a video file.

### (2) Who Will Do What
- **David:** Sentence caption feature tests and implementation
- **Krish:** Semantic similarity feature tests and implementation
- **Rachel:** Youtube option feature tests and implementation
- **Mahmoud:** GUI run_the_job() to connect frontend to backend (validate settings and start job from GUI); GUI framework and logic
- **Jeremy:** GUI framework and logic
- **Ralph:** update GUI
- **Michael:** update GUI
- **AK:** update GUI

### (3) Unit Test Cases
Note: Running the test cases is the same as for previous milestones. We have provided the same instructions below for convenience.
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
