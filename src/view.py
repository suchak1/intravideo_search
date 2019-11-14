from tkinter import *
from tkinter.filedialog import askopenfilename
import os
# -*- coding: utf-8 -*-

# set the default values for the GUI constructor.
DEFAULT = {'conf': .9, 'poll': 5, 'anti': 5, 'search': []}

class GUI:

    "Views - everything user sees"

    def __init__(self):
        # dictionary of key, val of key is string, val is int

        self.set_default_settings()
        self.job = None
        # this will be of class Job type, so not included in class diagram
        # but draw association arrow to Job Class

        #self.render()   # display GUI when this class instantiates

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

        expected_keys = ['conf', 'poll', 'anti', 'search']
        missing = [x for x in expected_keys if x not in values.keys()]
        if len(missing) > 0:
            self.set_default_settings()
            return False

        extra = [x for x in values.keys() if x not in expected_keys]
        if len(extra) > 0:
            self.set_default_settings()
            return False

        try:
            if not (isinstance(values['conf'], (int,float)) and isinstance(values['poll'], int) and isinstance(values['anti'], int)):
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

        if (values['conf'] < 0 or values['conf'] > 1 or values['poll'] < 0 or values['anti'] < 0 or values['search'] == []):
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

        lbl1 = Label(win, text= "Welcome to Intravideo Search!", font=("Times New Roman", 50), anchor="w")
        lbl1.grid(column=0, row=0)

        lbl2 = Label(win, text="Upload a video file.", justify=LEFT)
        lbl2.grid(sticky = W, column=0,row=1)

        def open_file():
            filename = askopenfilename()
            self.video_path = str(filename)

        button1 = Button(win, text="Upload", anchor="w", command=open_file)
        button1.grid(column=0, row=1)

        def change_confidence(val):
            self.settings['conf'] = float(val)/100

        def change_polling(val):
            self.settings['poll'] = int(val)

        def change_anti(val):
            self.settings['anti'] = int(val)

        lbl3 = Label(win, text="Confidence:", justify=LEFT)
        lbl3.grid(sticky = W, column=0, row=2)

        slider1 = Scale(win, from_=0, to=100, length = 200, orient=HORIZONTAL, command=change_confidence)
        slider1.set(self.settings['conf']*100)
        slider1.grid(sticky = W, column=1, row=2)

        lbl4 = Label(win, text="Polling Rate:", justify=LEFT)
        lbl4.grid(sticky = W, column=0, row=3)

        slider2 = Scale(win, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_polling)
        slider2.set(self.settings['poll'])
        slider2.grid(sticky = W, column=1, row=3)

        lbl5 = Label(win, text="Anti:", justify=LEFT)
        lbl5.grid(sticky = W, column=0, row=4)

        slider3 = Scale(win, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_anti)
        slider3.set(self.settings['anti'])
        slider3.grid(sticky = W, column=1, row=4)


        lbl6 = Label(win, text="Search Terms:", justify=LEFT)
        lbl6.grid(sticky=W, column=0, row=6)

        entry1 = Entry(win)
        entry1.grid(sticky=W, column=1, row=6)

        def entry1_delete():
            entry1.delete(first=0, last=100)

        def add_search_term():
            self.settings['search'].append(entry1.get())

        button2 = Button(win, text="Add", anchor='w', command=add_search_term)
        button2.grid(sticky=W, column=2, row=5)

        button3 = Button(win, text="Clear", anchor='w', command=entry1_delete)
        button3.grid(sticky=W, column=3, row=5)

        def display_settings():
            temp_lbl1 = Label(win, text="Settings: " + str(self.settings['conf']) + ", " + str(self.settings['poll']) + ", " + str(self.settings['anti']))
            temp_lbl1.grid(sticky=W, column=0, row=95)
            temp_lbl2 = Label(win, text="Search: ")
            temp_lbl2.grid(sticky=W, column=0, row=96)

            str1 = ''
            for ele in self.settings['search']:
                str1 += ', '
                str1 += ele

            temp_lbl4 = Label(win, text=str1)
            temp_lbl4.grid(sticky=W, column=1, row=96)
            temp_lbl3 = Label(win, text= "Video path: " + self.video_path)
            temp_lbl3.grid(sticky=W, column=0, row=97)


        display_settings_button = Button(win,text="Display Settings", command=display_settings)
        display_settings_button.grid(column=0, row=99)

        kill_button = Button(win,text="Kill this window", command= win.destroy)
        kill_button.grid(column=0, row=100)

        win.mainloop()
        return 0
