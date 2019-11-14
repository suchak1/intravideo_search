class Job:

    "Model - data logic"

    def __init__(self, settings=None):
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
        return []  # do whatever to get frames from vid as specific times using self.settings

    def classify_frames(self):
        frames = self.get_frames()
        results = [(self.score(Worker().classify_img(f)), t) for (f, t) in frames]
        return list(sorted(results, key=lambda x: x[1]))

    def score(self, confidence_dict):
        search_terms = self.settings['search']
        max_score = 0
        for term in search_terms:
            max_score = max(max_score, confidence_dict.get(term, 0))
        return max_score
        # use multiprocessing on loop in list comprehension below
        return [Worker.classify_img(frame) for frame in frames]

    def has_valid_args_interpret_results(self, results, cutoff):

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
        if len(results) == 0:
            return []

        positiveResults = []
        i = 0
        while(True):
            if i >= len(results):
                #print("Got to the end!")
                break
            if results[i][1] >= cutoff:
                #print("Found a goodie at {}!".format(i))
                foundEnd = False
                for j in range(i+1, len(results)):
                    if results[j][1] < cutoff:
                        #print("Found the end of it at {}!".format(j))
                        positiveResults.append((i, j))
                        foundEnd = True
                        break
                if foundEnd:
                    #print("Continuing on {}".format(j+1))
                    i = j+1
                    continue
                else:
                    #print("Did not find an end.")
                    positiveResults.append((i, -1))
                    break
            else:
                #print("Baddie at {}.".format(i))
                i += 1
                continue

        adjustedEndpoints = []
        for endpts in positiveResults:
            startIdx = endpts[0]
            endIdx = endpts[1]

            result1 = results[startIdx]
            result2 = results[endIdx]

            if startIdx == 0:
                #print("Starting at the start! startTime: 0.0")
                startTime = 0.0
            else:
                thisTime = result1[0]
                lastTime = results[startIdx-1][0]
                startTime = (thisTime + lastTime) / 2
                #print("thisTime {}, lastTime {}, startTime {}".format(thisTime, lastTime, startTime))

            if endIdx == -1:
                endTime = self.settings["runtime"]
                #print("Ending at the end. endTime {}".format(endTime))
            else:
                finalTime = results[endIdx-1][0]
                nextTime = results[endIdx][0]
                endTime = (finalTime + nextTime) / 2
                #print("thisTime {}, nextTime {}, endTime {}".format(finalTime, nextTime, endTime))

            adjustedEndpoints.append((startTime, endTime))

        #print(adjustedEndpoints)

        return adjustedEndpoints
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
