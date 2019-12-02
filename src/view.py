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
from multiprocessing import Process  # , Queue, Manager
import multiprocessing as mp
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

        valid = True
        error_list = list([])

        #all possible errors
        error_missing_keys = "ERROR: _ MISSING KEYS"
        error_extra_keys = "ERROR: _ EXTRA KEYS"
        error_no_conf = "ERROR: NO CONF"
        error_no_poll = "ERROR: NO POLL"
        error_no_anti = "ERROR: NO ANTI"
        error_no_runtime = "ERROR: NO RUNTIME"
        error_no_path = "ERROR: NO PATH"
        error_no_term = "ERROR: NO TERM"
        error_conf_out_of_range = "ERROR: YOUR CONF IS _, AND IT HAS TO BE BETWEEN 0 AND 1"
        error_poll_less_than_0 = "ERROR: YOUR POLL IS _, AND IT HAS TO BE GREATER THAN 0"
        error_anti_less_than_0 = "ERROR: YOUR ANTI IS _, AND IT HAS TO BE GREATER THAN 0"
        error_runtime_less_than_0 = "ERROR: YOUR RUNTIME IS _, AND IT HAS TO BE GREATER THAN 0"
        error_empty_search = "ERROR: EMPTY SEARCH"

        expected_keys = ['conf', 'poll', 'anti', 'runtime', 'search']
        missing = [x for x in expected_keys if x not in values.keys()]
        if len(missing) > 0:
            error_missing_keys = error_missing_keys.replace("_", str(len(missing)))
            self.set_default_settings()
            valid = False
            error_list.append(error_missing_keys)
            outcome = (valid, error_list)
            return outcome

        extra = [x for x in values.keys() if x not in expected_keys]
        if len(extra) > 0:
            error_extra_keys = error_extra_keys.replace("_", str(len(extra)))
            self.set_default_settings()
            return False
        try:
            if not (isinstance(values['conf'], (int,float)) and isinstance(values['poll'], int) and isinstance(values['anti'], int) and isinstance(values['runtime'], int)):
                raise TypeError

        try:
            if not (isinstance(values['conf'], (int,float))):
                error_list.append(error_no_conf)
            if not (isinstance(values['poll'], int)):
                error_list.append(error_no_poll)
            if not (isinstance(values['anti'], int)):
                error_list.append(error_no_anti)
            if not (isinstance(values['runtime'], int)):
                error_list.append(error_no_runtime)
            if not isinstance(path, str):
                error_list.append(error_no_path)
            if len(values['search']) != 0:
                for term in values['search']:
                    if not isinstance(term, str):
                        error_list.append(error_no_term)

            if len(error_list) > 0:
                raise TypeError

        except TypeError:
            self.set_default_settings()
            valid = False
            outcome = (valid, error_list)
            return outcome

        if (values['conf'] < 0 or values['conf'] > 1):
            error_conf_out_of_range = error_conf_out_of_range.replace("_", str(values["conf"]))
            error_list.append(error_conf_out_of_range)
        if (values['poll'] < 0):
            error_poll_less_than_0 = error_poll_less_than_0.replace("_", str(values["poll"]))
            error_list.append(error_poll_less_than_0)
        if (values['anti'] < 0):
            error_anti_less_than_0 = error_anti_less_than_0.replace("_", str(values["anti"]))
            error_list.append(error_anti_less_than_0)
        if (values['runtime'] < 0):
            error_runtime_less_than_0 = error_runtime_less_than_0.replace("_", str(values["runtime"]))
            error_list.append(error_runtime_less_than_0)
        if(values['search'] == []):
            error_empty_search = error_empty_search.replace("_", str(values["search"]))
            error_list.append(error_empty_search)

        if len(error_list) > 0:
            self.set_default_settings()
            valid = False
            outcome = (valid, error_list)
            return outcome

        self.settings = values  # be sure that values are always in the same order. Do validation
        self.video_path = path
        # where values is a dictionary

        outcome = (valid, error_list)
        return outcome

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
            entry0.delete(first=0, last=1000)
            temp_lbl3.configure(text="Video path: " + self.video_path)

        def del_youtube_link():
            entry0.delete(first=0, last=1000)

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

        '''
        You would need to set up a way to select output clips and then hit a button which produces
        a caption for it. The process would be: get the path of the clip, extract a frame from the
        middle of the clip, call the tell_us_oh_wise_one(frame) method from the Seer object which
        should be an attribute of GUI, and take the string it returns and print it to the GUI somewhere,
        '''

        temp_lbl4 = Label(win_content, text="", wraplength="200px", justify=CENTER)
        temp_lbl4.grid(column=3, row=100, columnspan=4)
        temp_lbl4.grid_remove()

        def get_caption():
            filename = askopenfilename()
            caption_videopath = str(filename)
            vid = cv2.VideoCapture(caption_videopath)
            total_frames = vid.get(7)
            vid.set(1,total_frames/2)
            ret, frame = vid.read()
            frame = Image.fromarray(frame)
            caption = self.seer.tell_us_oh_wise_one(frame)
            temp_lbl4.configure(text=caption)
            temp_lbl4.grid()
            select_button.configure(text="Clear Caption", command=clear_caption)

        def clear_caption():
            temp_lbl4.grid_remove()
            select_button.configure(text="Select Clip", command=get_caption)

        select_button = Button(win_content, text="Select Clip", anchor="w" , command=get_caption)
        select_button.grid(column=2, columnspan=3, row=99) #acknowledge that a file has been uploaded

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

        result = self.set_settings(settings, path)
        condition1 = result[0]
        if condition1 is False:
            msg += "Please double check your settings and try again.\n"
            for m in result[1]:
                msg += m + "\n"

        condition2 = os.path.isfile(path)
        if condition2 is False and not "youtube.com" in path:
            msg += "You entered an invalid file path. Please double check your input video and try again\n"
        else:
            condition2 = True

        if not condition1 or not condition2:
            return (False, msg)
          
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
