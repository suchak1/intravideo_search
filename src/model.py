import os
import cv2
from PIL import Image

class Job:

    "Model - data logic"

    def __init__(self, settings):
        if not isinstance(settings, type(None)):
            self.video_path = settings['video']
            self.settings = settings['settings']
            self.do_the_job()
        else:
            self.video_path = None
            self.settings = None

    def do_the_job(self):
        data = self.classify_frames()
        results = self.interpret_results(data)
        self.save_clips(results)

    def get_frames(self):
        # Given video and poll setting, returns list of tuples
        # where the first element is an Image of the frame from the video
        # at each timestamp designated by poll setting, and the second
        # element is the timestamp. For example, if poll is 5, get_frames()
        # will return a frame every 5 seconds at timestamps 0, 5, 10, etc.
        # seconds, i.e. it will return [(frame, 0), (frame, 5), (frame, 10)...]
        vidPath = self.video_path
        poll = self.settings['poll']
        count = 0
        frms = []
        video = cv2.VideoCapture(vidPath)
        success = True
        while success:
            timestamp = (count*poll)
            video.set(cv2.CAP_PROP_POS_MSEC, (timestamp*1000))
            success,frame = video.read()
            if success:
                cv2.imwrite('frame%d.jpg' % count, frame) # save frame as .jpg
                try:
                    f = Image.open('frame%d.jpg' % count) # make frame Image
                    os.remove('frame%d.jpg' % count) # delete frame.jpg
                    frms.append((f,timestamp))
                except:
                    raise NameError('getFrameError')
            count += 1
        return frms

    def classify_frames(self):
        '''
        frames = self.get_frames()
        # use multiprocessing on loop in list comprehension below
        return [Worker.classify_img(frame) for frame in frames]
        '''
        pass

    def interpret_results(self, results, cutoff=0.5):
        # Assuming arg: results is something like a list of tuples
        # of the form ((float)timestamp_t, (float)APIScore_t)
        # where APIScore_t is the score given by classify_frames()
        # to each frame_t fed through the API, normalized to be between [0,1].

        # Also assuming "endtime" is included in settings.

        return [(0.6, 666.6)]
        # where each timestamp is a tuple of start
        # time and end time, demarcating a sub-clip. A
        # positive result consits of a starttime, and
        # an endtime such that the starttime is above the
        # cutoff, all results in between the two are above
        # the cutoff, and the endtime is either the end of
        # the video or is below the cutoff. For endpoints
        # of start: t and end:t+10, where the first result
        # prior to t is t-2 and the first result prior
        # to t+10 is t-6, then the returned tuple should be:
        # ((t + (t-2))//2, ((t+10) + (t+6))//2)
        # => (t-1, t+8).
        # Special behavior at beginning and end,
        # if the first or last result is positive, the whole
        # first/last chunk of the video up until the
        # first result/endofthevideo is included.

    def save_clips(self, timestamps):
        # use multiprocessing here
        '''
        [Worker.make_clip(timestamp, self.video_path)
         for timestamp in timestamps]
        '''
        pass

    def kill(self):
        quit()
