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
from multiprocessing import Process, Queue, Manager
import sys
# -*- coding: utf-8 -*-


# set the default values for the GUI constructor.
DEFAULT = {'conf': .5, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []}
manager = Manager()
q = manager.Queue()


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
        self.queue = q

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
            # default checkmark state
            check = self.builder.get_object('Multi')
            if sys.platform == 'darwin':
                check.state(['disabled'])
                self.multi = None
            else:
                check.state(['!alternate'])
                check.state(['selected'])
                self.multi = True

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

    def handle_check_box(self):
        check_box = self.builder.get_object('Multi')
        checked = check_box.instate(['selected'])
        # if checked:
        #     check_box.state(['!selected'])
        # else:
        #     check_box.state(['selected'])
        if self.multi is not None:
            if checked:
                self.update_log('Multiprocessing enabled. Have fun :)')
                print('Multiprocessing enabled. WARNING: Fire possible.')
                self.multi = True
            else:
                self.update_log('Multiprocessing disabled. Afraid of fun?')
                print('Multiprocessing disabled. CRISIS AVERTED.')
                self.multi = False
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
                text.configure(state=tk.NORMAL)
                text.delete(1.0, tk.END)
                text.insert(1.0, caption)
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
        elif not isinstance(poll, int) or poll < 0 or poll > 60:
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
            if exitcode is not None:
                print('Process exited.')
                self.process.terminate()
                self.process.join()
                self.job.kill()
                self.job = None
                self.process = None
                self.builder.get_object('Start')['text'] = 'Start Job'
                pbar['value'] = 100
                num_vids = self.queue.get()
                if num_vids == 0:
                    self.update_log('SUCCESS: Job completed. No relevant clips found.')
                    self.builder.get_object('Status')['text'] = 'Done.'
                elif num_vids == -1:
                    self.update_log('OH DEAR: Some YouTube videos have squirrley encodings and this is one of them. Please try a different link.')
                    self.builder.get_object('Status')['text'] = 'Aborted.'
                else:
                    self.update_log(f'SUCCESS: Job completed. {num_vids} clips saved in source video path.')
                    self.builder.get_object('Status')['text'] = 'Done.'
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
            self.job = Job(settings, self.multi)
            self.update_log(f'PROCESSING: Processing job with settings: {settings}')
            btn = self.builder.get_object('Start')
            try:
                self.process = Process(target=self.job.do_the_job, args=(self.queue,))
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

    def close(self):
        if self.job:
            self.kill_job()
        self.master.destroy()


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
