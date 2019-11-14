import os
import tkinter as tk
# -*- coding: utf-8 -*-


DEFAULT = {'conf': .9, 'poll': 5, 'anti': 5, 'search': []}

class GUI:

    "Views - everything user sees"

    def __init__(self):
        # dictionary of key, val of key is string, val is int

        # Mahmoud and I talked this over and decided that this we would keep
        # these default values.
        self.set_default_settings()
        self.job = None
        # this will be of class Job type, so not included in class diagram
        # but draw association arrow to Job Class

        self.render()   # display GUI when this class instantiates

    def set_default_settings(self):
        self.settings = DEFAULT
        self.video_path = ''

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
        if not os.path.exists(path):
            self.set_default_settings()
            return False

        expected_keys = ['conf', 'poll', 'anti', 'search']
        missing = [x for x in expected_keys if x not in values.keys()]
        if len(missing) > 0:
            self.set_default_settings()
            return False

        extra = [x for x in values.keys() if x not in expected_keys]
        if len(extra) > 0:
            self.set_default_settings()
            return False

        if (values['conf'] < 0 or values['conf'] > 1 or values['poll'] < 0 or values['anti'] < 0 or values['search'] == []):
            self.set_default_settings()
            return False

        try:
            if not (isinstance(values['poll'], int) and isinstance(values['anti'], int)):
                raise TypeError

            for term in values['search']:
                if not isinstance(term, str):
                    raise TypeError
        except:
            self.set_default_settings()
            return False

        self.settings = values  # be sure that values are always in the same order. Do validation
        self.video_path = path
        # where values is a dictionary
        return True

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

        # win = tk.Tk()

        # win.title("Intravideo Search")
        # win.geometry("500x500")
        # tk.Label(win, text= "Video path: " + self.video_path).pack()
        # tk.Button(win,text="Upload").pack()

        # tk.Label(win, text="Settings: " + str(self.settings['conf']) + ", " + str(self.settings['poll']) + ", " + str(self.settings['anti']) + ", " + str(self.settings['search'])).pack()
        # tk.Button(win,text="Set").pack()

        # tk.Label(win, text="Set Poll Rate").pack()
        # tk.Button(win,text="Set").pack()

        # tk.Label(win, text="Type Search Term").pack()
        # tk.Button(win,text="Type").pack()

        # tk.Button(win,text="Kill this window", command= win.destroy).pack()

        # win.mainloop()
        return 0
