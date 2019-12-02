from model import Job, Seer
import tkinter as tk
from tkinter.ttk import *
from ttkthemes import ThemedTk
from tkinter.filedialog import askopenfilename
<<<<<<< HEAD
from playsound import playsound
import os
import subprocess
import time
import cv2
from PIL import Image
from model import Seer
=======
from PIL import Image
import os
import cv2
import pygubu
import re
from multiprocessing import Process  # , Queue, Manager
import multiprocessing as mp
>>>>>>> 9c484581f1024a3dd231d60d937b0ec6437b6578
# -*- coding: utf-8 -*-


# set the default values for the GUI constructor.
DEFAULT = {'conf': .5, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []}
# manager = Manager()
# q = manager.Queue()

class GUI:

    "Views - everything user sees"

    def __init__(self, master=None):

        # default settings
        self.set_default_settings()

        self.job = None
        self.process = None
        self.seer = Seer()
        self.prog_num = 0
        self.prog_len = 100
        self.master = master
        # self.queue = q

        # create builder
        self.builder = builder = pygubu.Builder()
        # load ui
        builder.add_from_file('src/gui.ui')
        # create root app
        if master:
            self.main_window = builder.get_object('Main_Window', master)
            # make gui unresizable
            master.resizable(0, 0)
            # connect callbacks
            builder.connect_callbacks(self)
            self.has_master = True
        else:
            self.has_master = False

    def set_default_settings(self):
        self.settings = DEFAULT
        self.video_path = ''

    def get_settings(self):
        # get settings currently in text boxes of GUI
        return {"video": self.video_path, "settings": self.settings}

    def on_browse_click(self):
        filename = str(askopenfilename())
        if filename:
            self.video_path = filename
            self.change_path_label(filename)
        self.update_log(f'Selected Video: {filename}')
        print(f'Selected Video: {self.video_path}')

    def change_path_label(self, filename):
        path_label = self.builder.get_object('Path_Label')
        if not self.check_yt_link(filename):
            filename = os.path.basename(filename)
        path_label.configure(text=filename)

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
        search = [term.strip() for term in terms.split(',')]
        self.settings['search'] = search
        print(search)
        self.update_log(f'Detected search terms: {search}')

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
        success = True
        msg = ''

        if not isinstance(conf, float) or conf < 0.0 or conf > 1.0:
            msg = f'ERROR: Invalid confidence level ({conf}).'
            success = False
        elif not isinstance(poll, int) or poll < 0 or poll > 150:
            msg = f'ERROR: Invalid polling rate ({poll}).'
            success = False
        elif (not isinstance(video_path, str) or
              not os.path.isfile(video_path) and
              not self.check_yt_link(video_path)):
            msg = f'ERROR: Invalid source video filepath or YouTube link ({video_path}).'
            success = False
        elif (not isinstance(search, list) or
              not len(search) or
              not any(re.search('[A-Za-z]', term) for term in search)):
            msg = f'ERROR: Invalid search terms detected ({search}).'
            success = False
        else:
            msg = f'SUCCESS: Settings {settings} verified.'

        if self.has_master:
            self.update_log(msg)
        return success

    def start_btn_handler(self):
        if self.job or self.process:
            self.kill_job()
        else:
            self.start_job()

    def get_progress(self):
        pbar = self.builder.get_object('Progressbar_1')
        job = self.job
        process = self.process
        if self.process:
            exitcode = self.process.exitcode
            print(exitcode)
            if exitcode is not None:
                self.process.terminate()
                self.process.join()
                self.job.kill()
                self.job = None
                self.process = None
                self.builder.get_object('Start')['text'] = 'Start Job'
                self.builder.get_object('Status')['text'] = 'Done.'
                pbar['value'] = 100
                if exitcode == 0:
                    self.update_log('SUCCESS: Job completed. No relevant clips found.')
                else:
                    self.update_log(f'SUCCESS: Job completed. {exitcode} clips saved in source video path.')
                return
            else:
                self.prog_num += 1
                val = int(round(self.prog_num % 100 / self.prog_len, 2) * 100)
                pbar['value'] = val
        else:
            pbar['value'] = int((self.prog_num / self.prog_len) * 100)
        self.master.after(50, self.get_progress)


    def kill_job(self):
        if self.job or self.process:
            try:
                print('Killing...')
                self.update_log('Killing...')
                self.process.terminate()
                self.job.kill()
                self.job = None
                self.process = None
                self.prog_num = 0
                print('Job killed successfully.')
                self.update_log('Job killed successfully.')
                self.builder.get_object('Start')['text'] = 'Start Job'
                self.builder.get_object('Status')['text'] = 'Waiting...'
            except:
                self.update_log('ERROR: Job could not be killed.')

    def start_job(self):
        self.parse_search_terms()
        if self.verify_settings():
            settings = self.get_settings()
            self.job = Job(settings)
            self.update_log(f'SUCCESS: Processing job with settings: {settings}')
            btn = self.builder.get_object('Start')
            try:
                self.process = Process(target=self.job.do_the_job)#, args=(self.queue,))
                btn['text'] = 'Cancel'
                self.builder.get_object('Status')['text'] = 'Working...'
                self.process.start()
                self.master.after(50, self.get_progress)
            except Exception as e:
                self.update_log(f'ERROR: Exception {e} occurred.')


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

        self.settings = values  # be sure that values are always in the same order. Do validation
        self.video_path = path
        # where values is a dictionary
        return True

    def construct_job(self):
        try:
            self.job = Job(self.get_settings())
            return True
        except:
            return False

    def remove_job(self):
        try:
            self.job.kill()
            return True
        except:
            return False

<<<<<<< HEAD
    def render(self):
        # display GUI, including text fields, choose file, and start button
        # also calls set_settings and start_job when start button is pressed

        win = Tk()

        win.title("Intravideo Search")
        win.geometry("960x540")
        win.resizable(0,0)
        win_header = Frame(win)
        win_header.pack()
        win_content = Frame(win)
        win_content.pack()


        #playsound('utils/TTFATF.mp3')
        #subprocess.call(["afplay", "TTFATF.mp3"])

        lbl1 = Label(win_header, text= "Welcome to Intravideo Search!", font=("Times New Roman", 50), anchor="w")
        lbl1.grid(column=0, row=0, columnspan=3)

        lbl2 = Label(win_content, text="Upload a video file", justify=LEFT)
        lbl2.grid(sticky = W, column=0,row=1)

        def open_file():
            filename = askopenfilename()
            self.video_path = str(filename)
            temp_lbl3.configure(text="Video path: " + str(filename))

        button1 = Button(win_content, text="Upload", anchor="w", command=open_file)
        button1.grid(column=1, row=1) #acknowledge that a file has been uploaded

        lbl0 = Label(win_content, text="or enter a YouTube link:", justify=LEFT)
        lbl0.grid(sticky = W, column=0,row=2)

        entry0 = Entry(win_content, width=30)
        entry0.grid(sticky=W, column=1, row=2, pady=10)

        def add_youtube_link():
            self.video_path = entry0.get()
            entry0.delete(first=0, last=100)

        def del_youtube_link():
            entry0.delete(first=0, last=100)

        button0 = Button(win_content, text="Add", anchor='w', command=add_youtube_link)
        button0.grid(sticky=W, column=3, row=2)

        button00 = Button(win_content, text="Clear", anchor='w', command=del_youtube_link)
        button00.grid(sticky=W, column=4, row=2)

        def change_confidence(val):
            self.settings['conf'] = float(val)/100
            settings_display_update()

        def change_polling(val):
            self.settings['poll'] = int(val)
            settings_display_update()

        def change_anti(val):
            self.settings['anti'] = int(val)
            settings_display_update()

        lbl3 = Label(win_content, text="Confidence:", justify=LEFT)
        lbl3.grid(sticky = E, column=0, row=3, padx=10)

        slider1 = Scale(win_content, from_=0, to=100, length = 200, orient=HORIZONTAL, command=change_confidence)
        slider1.set(self.settings['conf']*100)
        slider1.grid(sticky = W, column=1, row=3)

        lbl4 = Label(win_content, text="Polling Rate:", justify=LEFT)
        lbl4.grid(sticky = E, column=0, row=4, padx=10)

        slider2 = Scale(win_content, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_polling)
        slider2.set(self.settings['poll'])
        slider2.grid(sticky = W, column=1, row=4)

        lbl5 = Label(win_content, text="Anti:", justify=LEFT)
        lbl5.grid(sticky = E, column=0, row=5, padx=10)

        slider3 = Scale(win_content, from_=0, to=200, length = 200, orient=HORIZONTAL, command=change_anti)
        slider3.set(self.settings['anti'])
        slider3.grid(sticky = W, column=1, row=5)


        lbl6 = Label(win_content, text="Search Terms:", justify=LEFT)
        lbl6.grid(sticky=E, column=0, row=7, padx=10)

        entry1 = Entry(win_content, width=30)
        entry1.grid(sticky=W, column=1, row=7, pady=10)


        def update_search_display():
            temp_lbl2.configure(text="Search: " + search_display_terms())

        def search_display_terms():
            str1 = ''
            for ele in self.settings['search']:
                if ele and not ele.isspace():
                    str1 += ele
                    str1 += ', '
            return str1

        def settings_display_update():
            temp_lbl1.configure(text="Settings: " + str(self.settings['conf']) + ", " + str(self.settings['poll']) + ", " + str(self.settings['anti']) + ", " + str(self.settings['runtime']))

        temp_lbl1 = Label(win_content, text="Settings: " + str(self.settings['conf']) + ", " + str(self.settings['poll']) + ", " + str(self.settings['anti']) + ", " + str(self.settings['runtime']))
        temp_lbl1.grid(sticky=W, column=0, row=95)
        temp_lbl1.grid_remove()

        str1 = search_display_terms()
        temp_lbl2 = Label(win_content, text="Search: " + str1)
        temp_lbl2.grid(sticky=W, column=0, row=96)
        temp_lbl2.grid_remove()

        temp_lbl3 = Label(win_content, text= "Video path: " + self.video_path, wraplength="200px", justify=LEFT)
        temp_lbl3.grid(sticky=W, column=0, row=97, columnspan=2)
        temp_lbl3.grid_remove()

        def entry1_delete():
            entry1.delete(first=0, last=100)

        def get_search_term():
            my_string = entry1.get()
            result = [x.strip() for x in my_string.split(',')]
            self.settings['search'] = result

        def hide_settings():
            temp_lbl1.grid_remove()
            temp_lbl2.grid_remove()
            temp_lbl3.grid_remove()
            display_settings_button.configure(text="Display Settings", command=display_settings)

        def display_settings():
            display_settings_button.configure(text="Hide Settings", command=hide_settings)
            temp_lbl1.grid()
            temp_lbl2.grid()
            temp_lbl3.grid()

        display_settings_button = Button(win_content,text="Display Settings", command=display_settings)
        display_settings_button.grid(column=0, row=99, pady=10)

        kill_button = Button(win_content,text="Kill this window", command= win.destroy)
        kill_button.grid(column=0, row=100)

        def display_errors(title, message):
            w = Tk()
            w.title(title)
            w.geometry("800x170")
            content = Frame(w)
            content.pack()

            lbl = Label(content, text=message, font=("Times New Roman", 14), justify=LEFT)
            lbl.grid(column = 0, row = 0, columnspan=5)

            kill_button = Button(content,text="Ok", command= w.destroy)
            kill_button.grid(column=2, row=2)

        def run_the_job():
            update_search_display()
            get_search_term()
            start_button.config(state="disabled")
            bl, msg = self.run_job()
            display_captions(create_captions(create_frames()))

            if bl is False:
                display_errors(str(bl), msg)
                start_button.config(state="normal")

            else:
                msg2 = "Job cancelled"
                func = lambda:[self.job.kill, cancel_button.config(state="disabled"),display_errors("Cancelled", msg2)]
                cancel_button = Button(win_content,text="Cancel", command=func)
                cancel_button.grid(column=2,row=93) #kill this button once pressed?
                start_button.config(state="normal")

                try:
                    self.job.do_the_job() #We need to parallelize with the progress bar
                    display_errors("Success", "Processed Successfully")
                    ## add something about saving clips maybe
                    cancel_button.config(state="disabled")
                except e: #capture any errors that may occur
                    display_errors("Error", e)


        start_button = Button(win_content,text="Start", command=run_the_job)
        start_button.grid(column=1, row = 93)

        ## Stuff to do: create a list of subclips, create a Seer Class
        def create_frames():
            vidPath = self.video_path
            poll = self.settings['poll']
            count = 0
            frms = []
            video = cv2.VideoCapture(vidPath)
            success = True

            while success:
                timestamp = (count * poll)
                video.set(cv2.CAP_PROP_POS_MSEC, (timestamp * 1000))
                success, frame = video.read()
                if success:
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    frms.append((img, timestamp))
                count += 1
            return frms

        def create_captions(frames):
            captions = []
            for frm in frames:
                s = Seer()
                caption = s.tell_us_oh_wise_one(frm[0])
                captions.append((caption, frm[1]))
            return captions

        def display_captions(captions):
            win2 = Tk()

            win2.title("Possible Video Captions")
            win2.geometry("480x270")
            win2.resizable(0,0)
            win2_header = Frame(win2)
            win2_header.pack()
            win2_content = Frame(win2)
            win2_content.pack()

            lbl1 = Label(win2_header, text= "What's in this video?", font=("Times New Roman", 25), anchor="w")
            lbl1.grid(column=0, row=0, columnspan=3)

            lbl2 = Label(win2_content, text="Below are some possible captions to describe the video.", justify=LEFT)
            lbl2.grid(sticky = W, column=0,row=1)

            count = 2
            for c in captions:
                temp_lbl = Label(win2_content, text = c[0], justify=LEFT)
                temp_lbl.grid(sticky = W, column=0, row=count)
                count = count + 1

            win2.mainloop()
            return 0


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

        msg = ""
=======
    def close(self):
        if self.job:
            self.kill_job()
        self.master.destroy()
>>>>>>> 9c484581f1024a3dd231d60d937b0ec6437b6578


def render():
    root = ThemedTk(theme='arc')
    app = GUI(root)
    root.protocol('WM_DELETE_WINDOW', app.close)
    root.mainloop()

# multiprocessing checkbox support
# default is off on mac, on otherwise
# disabled button, checked otherwise
# if checked, can check on and off which updates multi val
# which gets passes in job constructor Job(multi=True)
# use that val in job unless mac, then block (false)

# read article about progress bars
