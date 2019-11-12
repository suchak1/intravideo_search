from tkinter import *
# -*- coding: utf-8 -*-


class GUI:

    "Views - everything user sees"

    def __init__(self):
        self.video_path = ''  # string file path
        # dictionary of key, val of key is string, val is int

        # Mahmoud and I talked this over and decided that this we would keep
        # these default values.
        self.settings = {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""]}
        self.job = None
        # this will be of class Job type, so not included in class diagram
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
        return False
        self.settings = values  # be sure that values are always in the same order. Do validation
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

        win = Tk()

        win.title("Intravideo Search")
        win.geometry("960x540")

        # tk.Label(win, text= "Video path: " + self.video_path).pack()
        # tk.Button(win,text="Upload").pack()

        # tk.Label(win, text="Settings: " + str(self.settings['conf']) + ", " + str(self.settings['poll']) + ", " + str(self.settings['anti']) + ", " + str(self.settings['search'])).pack()
        # tk.Button(win,text="Set").pack()

        # tk.Label(win, text="Set Poll Rate").pack()
        # tk.Button(win,text="Set").pack()

        # tk.Label(win, text="Type Search Term").pack()
        # tk.Button(win,text="Type").pack()

        lbl1 = Label(win, text= "Welcome to Intravideo Search!", font=("Times New Roman", 50), anchor="w")
        lbl1.grid(column=0, row=0)

        lbl2 = Label(win, text="Upload a video file.", justify=LEFT)
        lbl2.grid(sticky = W, column=0,row=1)

        button1 = Button(win, text="Upload", anchor="w")
        button1.grid(column=0, row=1)

        lbl3 = Label(win, text="Confidence:", justify=LEFT)
        lbl3.grid(sticky = W, column=0, row=2)

        slider1 = Scale(win, from_=0, to=100, length = 200, orient=HORIZONTAL)
        slider1.grid(sticky = W, column=1, row=2)

        lbl4 = Label(win, text="Polling Rate:", justify=LEFT)
        lbl4.grid(sticky = W, column=0, row=3)

        slider2 = Scale(win, from_=0, to=200, length = 200, orient=HORIZONTAL)
        slider2.grid(sticky = W, column=1, row=3)

        lbl5 = Label(win, text="Anti:", justify=LEFT)
        lbl5.grid(sticky = W, column=0, row=4)

        slider3 = Scale(win, from_=0, to=200, length = 200, orient=HORIZONTAL)
        slider3.grid(sticky = W, column=1, row=4)

        lbl6 = Label(win, text="Search Terms:", justify=LEFT)
        lbl6.grid(sticky=W, column=0, row=5)

        entry1 = Entry(win)
        entry1.grid(sticky=W, column=1, row=5)

        button2 = Button(win, text="Add", anchor='w')
        button2.grid(sticky=W, column=2, row=5)

        button3 = Button(win, text="Clear", anchor='w')
        button3.grid(sticky=W, column=3, row=5)


        kill_button = Button(win,text="Kill this window", command= win.destroy)
        kill_button.grid(column=0, row=100)

        win.mainloop()
        return 0

test_gui = GUI()
