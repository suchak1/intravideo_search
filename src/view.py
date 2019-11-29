from model import Job, Seer
import tkinter as tk
from tkinter.ttk import *
from ttkthemes import ThemedTk
from tkinter.filedialog import askopenfilename
from PIL import Image
import os
import cv2
import pygubu
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
            print('Not a valid YouTube link')
            return
        print(f'Selected Video: {self.video_path}')

    def del_youtube_link(self):
        yt_entry = self.builder.get_object('YouTube_Entry')
        end = len(str(yt_entry.get()))
        yt_entry.delete(0, end)
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

def render():
    root = ThemedTk(theme='arc')
    app = Application(root)
    root.mainloop()

render()


    #     temp_lbl1 = Label(win_content, text="Settings: " + str(self.settings['conf']) + ", " + str(self.settings['poll']) + ", " + str(self.settings['anti']) + ", " + str(self.settings['runtime']))
    #     temp_lbl1.grid(sticky=W, column=0, row=95)
    #     temp_lbl1.grid_remove()
    #
    #
    #     def change_confidence(val):
    #         self.settings['conf'] = round(float(val)/100, 2)
    #         settings_display_update()
    #
    #     def change_polling(val):
    #         self.settings['poll'] = int(float(val))
    #         settings_display_update()
    #
    #     slider2 = Scale(win_content, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_polling)
    #     slider2.set(self.settings['poll'])
    #     slider2.grid(sticky = W, column=1, row=4)
    #
    #     # lbl5 = Label(win_content, text="Anti:", justify=LEFT)
    #     # lbl5.grid(sticky = E, column=0, row=5, padx=10)
    #     #
    #     # slider3 = Scale(win_content, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_anti)
    #     # slider3.set(self.settings['anti'])
    #     # slider3.grid(sticky = W, column=1, row=5)
    #
    #
    #     lbl6 = Label(win_content, text="Search Terms:", justify=LEFT)
    #     lbl6.grid(sticky=E, column=0, row=7, padx=10)
    #
    #     entry1 = Entry(win_content, width=30)
    #     entry1.grid(sticky=W, column=1, row=7, pady=10)
    #
    #     def update_search_display():
    #         temp_lbl2.configure(text="Search: " + search_display_terms())
    #
    #     def search_display_terms():
    #         str1 = ''
    #         for ele in self.settings['search']:
    #             if ele and not ele.isspace():
    #                 str1 += ele
    #                 str1 += ', '
    #         return str1
    #
    #
    #
    #
    #     str1 = search_display_terms()
    #     temp_lbl2 = Label(win_content, text="Search: " + str1)
    #     temp_lbl2.grid(sticky=W, column=0, row=96)
    #     temp_lbl2.grid_remove()
    #
    #     temp_lbl3 = Label(win_content, text= "Video path: " + self.video_path, wraplength="200px", justify=LEFT)
    #     temp_lbl3.grid(sticky=W, column=0, row=97, columnspan=2)
    #     temp_lbl3.grid_remove()
    #
    #     def entry1_delete():
    #         entry1.delete(first=0, last=100)
    #
    #     def get_search_term():
    #         my_string = entry1.get()
    #         result = [x.strip() for x in my_string.split(',')]
    #         self.settings['search'] = result
    #
    #     def hide_settings():
    #         temp_lbl1.grid_remove()
    #         temp_lbl2.grid_remove()
    #         temp_lbl3.grid_remove()
    #         display_settings_button.configure(text="Display Settings", command=display_settings)
    #
    #     def display_settings():
    #         display_settings_button.configure(text="Hide Settings", command=hide_settings)
    #         temp_lbl1.grid()
    #         temp_lbl2.grid()
    #         temp_lbl3.grid()
    #
    #     display_settings_button = Button(win_content,text="Display Settings", command=display_settings)
    #     display_settings_button.grid(column=0, row=99, pady=10)
    #
    #
    #     '''
    #     You would need to set up a way to select output clips and then hit a button which produces
    #     a caption for it. The process would be: get the path of the clip, extract a frame from the
    #     middle of the clip, call the tell_us_oh_wise_one(frame) method from the Seer object which
    #     should be an attribute of GUI, and take the string it returns and print it to the GUI somewhere,
    #     '''
    #
    #     temp_lbl4 = Label(win_content, text="", wraplength="200px", justify=CENTER)
    #     temp_lbl4.grid(column=3, row=100, columnspan=4)
    #     temp_lbl4.grid_remove()
    #
    #     def get_caption():
    #         filename = askopenfilename()
    #         caption_videopath = str(filename)
    #         vid = cv2.VideoCapture(caption_videopath)
    #         total_frames = vid.get(7)
    #         vid.set(1,total_frames/2)
    #         ret, frame = vid.read()
    #         frame = Image.fromarray(frame)
    #         caption = self.seer.tell_us_oh_wise_one(frame)
    #         temp_lbl4.configure(text=caption)
    #         temp_lbl4.grid()
    #         select_button.configure(text="Clear Caption", command=clear_caption)
    #
    #     def clear_caption():
    #         temp_lbl4.grid_remove()
    #         select_button.configure(text="Select Clip to Caption", command=get_caption)
    #
    #     select_button = Button(win_content, text="Select Clip to Caption", command=get_caption)
    #     select_button.grid(column=2, columnspan=3, row=99) #acknowledge that a file has been uploaded
    #
    #     def display_errors(title, message):
    #         w = Tk()
    #         w.title(title)
    #         w.geometry("800x170")
    #         content = Frame(w)
    #         content.pack()
    #
    #         lbl = Label(content, text=message, font=("Times New Roman", 14), justify=LEFT)
    #         lbl.grid(column = 0, row = 0, columnspan=5)
    #
    #
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
    # def run_job(self):
    #     """
    #     Validates the settings of the GUI and makes sure that they are valid
    #     Ensures that the video path given is a valid video and can be opened by the application
    #     Returns a tuple: (bool, msg) where bool is True if everything is valid and a Job was started and False otherwise,
    #     and msg is a success or error message
    #     """
    #     settings = self.settings
    #     path = self.video_path
    #
    #     msg = ""
    #
    #     condition1 = self.set_settings(settings, path)
    #     if condition1 is False:
    #         msg += "One or more of your settings parameters are invalid. Please double check your settings and try again\n"
    #         #maybe which settings are off?
    #
    #     condition2 = os.path.isfile(path)
    #     if condition2 is False and not "youtube.com" in path:
    #         msg += "You entered an invalid file path. Please double check your input video and try again\n"
    #     else:
    #         condition2 = True
    #
    #     if not condition1 or not condition2:
    #         return(False, msg)
    #
    #     self.job = Job(self.get_settings())
    #     return (True, "Success")
