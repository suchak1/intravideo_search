from model import Job
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
# -*- coding: utf-8 -*-

# set the default values for the GUI constructor.
DEFAULT = {'conf': .9, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []}

class GUI:

    "Views - everything user sees"

    def __init__(self):
        # dictionary of key, val of key is string, val is int

        self.set_default_settings()
        self.job = None
        # this will be of class Job type, so not included in class diagram
        # but draw association arrow to Job Class

        # self.render()   # display GUI when this class instantiates

    def set_default_settings(self):
        self.settings = DEFAULT
        self.video_path = ''

    def get_settings(self):
        # get settings currently in text boxes of GUI
        return {"video": self.video_path, "settings": self.settings}

    def set_settings(self, values, path):

        #Sets the settings of the GUI and includes the video path file.

        #values is a dictionary in the following format:
        #        'conf': float,
        #        'poll': int,
        #        'anti': int,
        #        'search': list of strings
        #    }
        #   'conf': confidence interval for image classification. Must be a value between 0 and 1
        #    'poll': the framerate poll (frequency of frames to classify). Must be a value >= 0
        #    'anti': the treshold for how long a clip can contain frames not containing the search question
        #            (anything longer will be the bounds of the clip). Must be a value >= 0
        #    'search': a list of search terms to use. Must contain at least one string.

        # path is the video_input path

        #if not os.path.exists(path):
        #    print('Here1')
            #self.set_default_settings()
        #    return False
        #print(len(values['search']))
        #print(values['search'][0])
        #print(path)
        #print(type(path))

        expected_keys = ['conf', 'poll', 'anti', 'runtime', 'search']
        missing = [x for x in expected_keys if x not in values.keys()]
        if len(missing) > 0:
            self.set_default_settings()
            return False

        extra = [x for x in values.keys() if x not in expected_keys]
        if len(extra) > 0:
            self.set_default_settings()
            return False

        try:
            if not (isinstance(values['conf'], (int,float)) and isinstance(values['poll'], int) and isinstance(values['anti'], int) and isinstance(values['runtime'], int)):
                raise TypeError

            if not isinstance(path, str):
                raise TypeError

            if len(values['search']) != 0:
                for term in values['search']:
                    if not isinstance(term, str):
                        raise TypeError

        except TypeError:
            self.set_default_settings()
            return False

        if (values['conf'] < 0 or values['conf'] > 1 or values['poll'] < 0 or values['anti'] < 0 or values['runtime'] < 0 or values['search'] == []):
            self.set_default_settings()
            return False

        #print('values: ' + str(values))
        self.settings = values  # be sure that values are always in the same order. Do validation
        #print('self.settings: ' + str(self.settings))
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

        win = Tk()

        win.title("Intravideo Search")
        win.geometry("960x540")
        win_header = Frame(win)
        win_header.pack()
        win_content = Frame(win)
        win_content.pack()

        lbl1 = Label(win_header, text= "Welcome to Intravideo Search!", font=("Times New Roman", 50), anchor="w")
        lbl1.grid(column=0, row=0, columnspan=3)

        lbl2 = Label(win_content, text="Upload a video file.", justify=LEFT)
        lbl2.grid(sticky = W, column=0,row=1)

        def open_file():
            filename = askopenfilename()
            self.video_path = str(filename)

        button1 = Button(win_content, text="Upload", anchor="w", command=open_file)
        button1.grid(column=1, row=1)

        def change_confidence(val):
            self.settings['conf'] = float(val)/100

        def change_polling(val):
            self.settings['poll'] = int(val)

        def change_anti(val):
            self.settings['anti'] = int(val)

        lbl3 = Label(win_content, text="Confidence:", justify=LEFT)
        lbl3.grid(sticky = E, column=0, row=2, padx=10)

        slider1 = Scale(win_content, from_=0, to=100, length = 200, orient=HORIZONTAL, command=change_confidence)
        slider1.set(self.settings['conf']*100)
        slider1.grid(sticky = W, column=1, row=2)

        lbl4 = Label(win_content, text="Polling Rate:", justify=LEFT)
        lbl4.grid(sticky = E, column=0, row=3, padx=10)

        slider2 = Scale(win_content, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_polling)
        slider2.set(self.settings['poll'])
        slider2.grid(sticky = W, column=1, row=3)

        lbl5 = Label(win_content, text="Anti:", justify=LEFT)
        lbl5.grid(sticky = E, column=0, row=4, padx=10)

        slider3 = Scale(win_content, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_anti)
        slider3.set(self.settings['anti'])
        slider3.grid(sticky = W, column=1, row=4)


        lbl6 = Label(win_content, text="Search Terms:", justify=LEFT)
        lbl6.grid(sticky=E, column=0, row=6, padx=10)

        entry1 = Entry(win_content, width=30)
        entry1.grid(sticky=W, column=1, row=6, pady=10)

        def entry1_delete():
            entry1.delete(first=0, last=100)

        def add_search_term():
            self.settings['search'].append(entry1.get())

        button2 = Button(win_content, text="Add", anchor='w', command=add_search_term)
        button2.grid(sticky=W, column=3, row=6)

        button3 = Button(win_content, text="Clear", anchor='w', command=entry1_delete)
        button3.grid(sticky=W, column=4, row=6)

        def display_settings():
            temp_lbl1 = Label(win_content, text="Settings: " + str(self.settings['conf']) + ", " + str(self.settings['poll']) + ", " + str(self.settings['anti']) + ", " + str(self.settings['runtime']))
            temp_lbl1.grid(sticky=W, column=0, row=95)
            temp_lbl2 = Label(win_content, text="Search: ")
            temp_lbl2.grid(sticky=W, column=0, row=96)

            str1 = ''
            for ele in self.settings['search']:
                str1 += ', '
                str1 += ele

            temp_lbl4 = Label(win_content, text=str1)
            temp_lbl4.grid(sticky=W, column=1, row=96)
            temp_lbl3 = Label(win_content, text= "Video path: " + self.video_path, wraplength="200px", justify=LEFT)
            temp_lbl3.grid(sticky=W, column=0, row=97, columnspan=2)


        display_settings_button = Button(win_content,text="Display Settings", command=display_settings)
        display_settings_button.grid(column=0, row=99, pady=10)

        kill_button = Button(win_content,text="Kill this window", command= win.destroy)
        kill_button.grid(column=0, row=100)

        win.mainloop()
        return 0

    def run_job(self):
        """
        Validates the settings of the GUI and makes sure that they are valid
        Ensures that the video path given is a valid video and can be opened by the application
        Returns a tuple: (bool, msg) where bool is True if everything is valid and a Job was started and False otherwise,
        and msg is a success or error message
        """
        settings = self.settings
        path = self.video_path

        return (True, "Success")


