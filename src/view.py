class GUI:

    "Views - everything user sees"

    def __init__(self):
        self.video_path = ''  # string file path
        self.settings = {}  # dictionary of key, val of key is string, val is int
        #initialize default settings

        self.job = None  # this will be of class Job type, so not included in class diagram
        # but draw association arrow to Job Class

        self.render()   # display GUI when this class instantiates

    def get_settings(self):
        # get settings currently in text boxes of GUI
        return {"video": self.video_path, "settings": self.settings}

    def set_settings(self, values, path):
        """
        Sets the settings of the GUI and includes the video path file.

        values is a dictionary in the following format:
            {
                'conf': float,
                'poll': int,
                'anti': int,
                'search': list of strings
            }
        `   'conf': confidence interval for image classification. Must be a value between 0 and 1
            'poll': the framerate poll (frequency of frames to classify). Must be a value >= 0
            'anti': the treshold for how long a clip can contain frames not containing the search question
                    (anything longer will be the bounds of the clip). Must be a value >= 0
            'search': a list of search terms to use. Must contain at least one string.

        path is the video_input path
        """
        self.settings = values #be sure that values are always in the same order. Do validation
        self.video_path = path
        # where values is a dictionary
        return False

    def start_job(self):
        self.job = Job(self.get_settings())

    def kill_job(self):
        self.job.kill()

    def render(self):
        # display GUI, including text fields, choose file, and start button
        # also calls set_settings and start_job when start button is pressed
        return 0
