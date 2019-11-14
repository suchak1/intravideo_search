from controller import Worker
import os
import sys
import cv2
from PIL import Image
#from multiprocessing import Pool

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
        #self.save_clips(results)

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
        frames = self.get_frames()
        results = [(self.score(Worker().classify_img(f)), t) for (f, t) in frames]
        norm = 100
        results = [(val / norm, t) for (val, t) in results]
        return list(sorted(results, key=lambda x: x[1]))

    def score(self, confidence_dict):
        search_terms = self.settings['search']
        max_score = 0
        for term in search_terms:
            max_score = max(max_score, confidence_dict.get(term, 0))
        return max_score

    def has_valid_args_interpret_results(self, results, cutoff):
        # This is a very simple helper function which throws an exception
        # in the case of invalid arguments. The functionality of this is
        # sufficiently tested in the tests of the interpret_results() function.

        if not isinstance(results, type([])):
            raise TypeError("Expected List. Got {}".format(type(results)))
        timeSet = set()
        for elt in results:
            if elt[0] < 0:
                raise ValueError("Negative time stamp in results. Please don't do that. Got {}".format(elt[0]))
            if elt[1] < 0:
                raise ValueError("Negative score in results. Don't do this to me. Got {}".format(elt[1]))
            if elt[1] > 1:
                raise ValueError("Un-normalized score in results. Got {}, expected value in [0,1]".format(elt[1]))
            if elt[0] in timeSet:
                raise ValueError("Duplicate times in results. Found more than one of: {}".format(elt[0]))
            else:
                timeSet.add(elt[0])
            if elt[0] < sorted(list(timeSet))[-1]:
                raise ValueError("Results given out of order. I could fix this, but \
                this probably means something is funky with whatever process produced this.")
            if cutoff < 0:
                raise ValueError("Cutoff parameter less than zero. Got: {}".format(cutoff))

    def interpret_results(self, results, cutoff=0.5):
        # Assuming arg: results is something like a list of tuples
        # of the form ((float)timestamp_t, (float)APIScore_t)
        # where APIScore_t is the score given by classify_frames()
        # to each frame_t fed through the API, normalized to be between [0,1].
        # Also assuming "runtime" is included in settings.

        # Checking that the arguments are valid.
        self.has_valid_args_interpret_results(results, cutoff)

        # If there are no results, return an empty list.
        if len(results) == 0:
            return []

        # For each positive result, find the proper start/end times of the
        # relevant sub-clip.
        positiveResults = []
        i = 0
        while(True):
            if i >= len(results):
                break
            if results[i][1] >= cutoff:
                foundEnd = False
                for j in range(i+1, len(results)):
                    if results[j][1] < cutoff:
                        positiveResults.append((i, j))
                        foundEnd = True
                        break
                if foundEnd:
                    i = j+1
                    continue
                else:
                    positiveResults.append((i, -1))
                    break
            else:
                i += 1
                continue

        # Adjust those times to fit in the midpoint of the polled frames,
        # for a smoother results.
        adjustedEndpoints = []
        for endpts in positiveResults:
            startIdx = endpts[0]
            endIdx = endpts[1]

            result1 = results[startIdx]
            result2 = results[endIdx]

            if startIdx == 0:
                startTime = 0.0
            else:
                thisTime = result1[0]
                lastTime = results[startIdx-1][0]
                startTime = (thisTime + lastTime) / 2

            if endIdx == -1:
                endTime = self.settings["runtime"]
            else:
                finalTime = results[endIdx-1][0]
                nextTime = results[endIdx][0]
                endTime = (finalTime + nextTime) / 2

            adjustedEndpoints.append((startTime, endTime))

        return adjustedEndpoints


    def save_clips(self, timestamps):
        #with Pool() as pool:
        #    v = self.video_path
        #    args_list = [(t, v) for t in timestamps]
        #    map_results = pool.starmap(Worker().make_clip, args_list)

        #return map_results
        # multiprocessing is running into issues with shared resources
        v = self.video_path
        return [Worker().make_clip(t, v) for t in timestamps]


    def kill(self):
        del self
