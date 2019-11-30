from model import Job, Seer
import tkinter as tk
from tkinter.ttk import *
from ttkthemes import ThemedTk
from tkinter.filedialog import askopenfilename
from PIL import Image
import os
import cv2
import pygubu
import re
# -*- coding: utf-8 -*-

# set the default values for the GUI constructor.
DEFAULT = {'conf': .9, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []}

class GUI:

    "Views - everything user sees"

    def __init__(self, master):
        # dictionary of key, val of key is string, val is int

        self.set_default_settings()
        self.job = None
        self.seer = Seer()
        # this will be of class Job type, so not included in class diagram
        # but draw association arrow to Job Class

        # self.render()   # display GUI when this class instantiates
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('src/gui.ui')
        self.mainwindow = builder.get_object('Main_Window', master)

    def set_default_settings(self):
        self.settings = DEFAULT
        self.video_path = ''

    def get_settings(self):
        # get settings currently in text boxes of GUI
        return {"video": self.video_path, "settings": self.settings}

    def set_settings(self, values, path):
        # Sets the settings of the GUI and includes the video path file.
        expected_keys = ['conf', 'poll', 'anti', 'runtime', 'search']
        missing = [x for x in expected_keys if x not in values.keys()]
        if len(missing) > 0:
            self.set_default_settings()
            return False

        extra = [x for x in values.keys() if x not in expected_keys]
        if len(extra) > 0:
            self.set_default_settings()
            return False
        # values['runtime'] = int(values['runtime'])
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

        root = ThemedTk(theme='arc')
        self.GUI(master=root)
        root.mainloop()
class Application:
    def __init__(self, master):

        # default settings
        self.settings = {
            'poll': 5,
            'anti': 5,
            'conf': .5,
            'search': [],
            'runtime': 1
        }

        self.video_path = ''

        self.job = None
        self.seer = Seer()

        # create builder
        self.builder = builder = pygubu.Builder()
        # load ui
        builder.add_from_file('src/gui.ui')
        # create root app
        self.main_window = builder.get_object('Main_Window', master)
        # make gui unresizable
        master.resizable(0, 0)
        # connect callbacks
        builder.connect_callbacks(self)

    def on_browse_click(self):
        filename = str(askopenfilename())
        if filename:
            self.video_path = filename
            self.change_path_label(filename)
        print(f'Selected Video: {self.video_path}')

    def change_path_label(self, filename):
        path_label = self.builder.get_object('Path_Label')
        file = os.path.basename(filename)
        path_label.configure(text=file)

    def check_yt_link(self, link):
        return 'youtube.com' in link or 'youtu.be/' in link

    def add_youtube_link(self):
        yt_entry = self.builder.get_object('YouTube_Entry')
        link = str(yt_entry.get()).strip()
        if self.check_yt_link(link):
            self.video_path = link
            self.change_path_label(link)
        else:
            print('Not a valid YouTube link.')
            self.update_log('ERROR: Please enter a valid YouTube link.')
            return
        print(f'Selected Video: {self.video_path}')

    def del_youtube_link(self):
        yt_entry = self.builder.get_object('YouTube_Entry')
        yt_entry.delete(0, tk.END)
        if self.check_yt_link(self.video_path):
            self.video_path = None
            self.change_path_label('None')
            print('YouTube link cleared from job.')
        else:
            print('YouTube link cleared from entry field.')

    def change_poll(self, val):
        val = int(float(val))
        poll = self.builder.get_object('Poll_Num')
        poll.configure(text=f'{val} sec')
        self.settings['poll'] = val

    def change_conf(self, val):
        val = round(float(val) / 100, 2)
        conf = self.builder.get_object('Conf_Level')
        conf.configure(text=f'{int(val * 100)}%')
        self.settings['conf'] = val

    def parse_search_terms(self):
        search_entry = self.builder.get_object('Search_Entry')
        terms = str(search_entry.get())
        search = [term.strip() for term in terms]
        self.settings['search'] = search
        print(search)

    # need to add handler for multiprocessing checkmark
    # and make multi attribute for job that is true by default

    def handle_caption_btn(self):
        btn = self.builder.get_object('Caption_Button')
        text = self.builder.get_object('Caption_Text')
        if btn['text'] == 'Choose Clip':
            self.get_caption(btn, text)
        else:
            self.clear_caption(btn, text)

    def clear_caption(self, btn, text):
        text.configure(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.configure(state=tk.DISABLED)
        btn['text'] = 'Choose Clip'

    def get_caption(self, btn, text):
        filename = str(askopenfilename())
        if filename:
            video = cv2.VideoCapture(filename)
            total_frames = video.get(7)
            video.set(1, total_frames / 2)
            ret, frame = video.read()
            if ret:
                frame = Image.fromarray(frame)
                caption = str(self.seer.tell_us_oh_wise_one(frame))
                mid = int(len(caption) // 2)
                wrapped = caption[:mid] + '-\n' + caption[mid:]
                text.configure(state=tk.NORMAL)
                text.delete(1.0, tk.END)
                text.insert(1.0, wrapped)
                text.configure(state=tk.DISABLED)
                btn['text'] = 'Clear Caption'

    def update_log(self, update):
        text = self.builder.get_object('Log')
        text.configure(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(1.0, update)
        text.configure(state=tk.DISABLED)

    def verify_settings(self):
        settings = self.settings
        video_path = self.video_path

        conf = settings['conf']
        poll = settings['poll']
        search = settings['search']

        if not isinstance(conf, float) or conf < 0.0 or conf > 1.0:
            self.update_log('ERROR: Invalid confidence level.')
            return False
        elif not isinstance(poll, int) or poll < 0 or poll > 150:
            self.update_log('ERROR: Invalid polling rate.')
            return False
        elif (not isinstance(search, str) or
              not os.path.isfile(video_path) and
              not self.check_yt_link(video_path)):
            self.update_log('ERROR: Invalid source video filepath or YouTube link.')
            return False
        elif (not isinstance(search, list) or
              not len(search) or
              not any(re.search('[A-Za-z]', term) for term in search)):
            self.update_log('ERROR: Invalid search terms detected.')
            return False
        else:
            self.update_log(f'SUCCESS: Settings {settings} verified.')
            return True


def render():
    root = ThemedTk(theme='arc')
    app = Application(root)
    root.mainloop()

render()
# verify_settings
# check that search terms aren't empty and have at least one alphabetic letter

# run job
# attach start button
# self.settings['search'] = self.parse_search_terms
# then verify_settings
# if true: say processing job and do job else: error
# decide for cancel button

# multiprocessing checkbox support
# default is off on mac, on otherwise
# disabled button, checked otherwise
# if checked, can check on and off which updates multi val
# which gets passes in job constructor Job(multi=True)
# use that val in job unless mac, then block (false)

# read article about progress bars

    #     def run_the_job():
    #         update_search_display()
    #         get_search_term()
    #         start_button.config(state="disabled")
    #         bl, msg = self.run_job()
    #
    #         if bl is False:
    #             display_errors(str(bl), msg)
    #             start_button.config(state="normal")
    #
    #         else:
    #             msg2 = "Job cancelled"
    #             func = lambda:[self.job.kill, cancel_button.config(state="disabled"),display_errors("Cancelled", msg2)]
    #             cancel_button = Button(win_content,text="Cancel", command=func)
    #             cancel_button.grid(column=2,row=93) #kill this button once pressed?
    #             start_button.config(state="normal")
    #
    #             try:
    #                 self.job.do_the_job() #We need to parallelize with the progress bar
    #                 display_errors("Success", "Processed Successfully")
    #                 ## add something about saving clips maybe
    #                 cancel_button.config(state="disabled")
    #             except e: #capture any errors that may occur
    #                 display_errors("Error", e)
    #
    #     start_button = Button(win_content,text="Start", command=run_the_job)
    #     start_button.grid(column=1, row = 93)
    #
    #     win.mainloop()
    #     return 0
    #
