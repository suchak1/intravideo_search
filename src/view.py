class GUI:

    "Views - everything user sees"

    def __init__(self):
        self.video_path = ''  # string file path
        self.settings = {}  # dictionary of key, val of key is string, val is int
        self.job = None  # this will be of class Job type, so not included in class diagram
        # but draw association arrow to Job Class

        self.render()   # display GUI when this class instantiates

    def get_settings(self):
        # get settings currently in text boxes of GUI
        return {video: self.video_path, settings: self.settings}

    def set_settings(self, values, path):
        self.settings = values
        self.video_path = path
        # where values is a dictionary

    def start_job(self):
        try:
            self.job = Job(self.get_settings())
            return True
        except:
            return False

    def kill_job(self):
        try:
            self.job.kill()
            return True
        except:
            return False

    def render(self):
        # display GUI, including text fields, choose file, and start button
        # also calls set_settings and start_job when start button is pressed
        return 0
