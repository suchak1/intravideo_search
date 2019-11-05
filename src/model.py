class Job:

    "Model - data logic"

    def __init__(self, settings=None):
        self.video_path = settings.video_path
        self.settings = settings.settings


    def do_the_job(self):
        data = self.classify_frames()
        results = self.interpret_results(data)
        save_clips(results)


    def get_frames(self):
        return 0  # do whatever to get frames from vid as specific times using self.settings


    def classify_frames(self):
        frames = self.get_frames()
        # use multiprocessing on loop in list comprehension below
        return [Worker.classify_img(frame) for frame in frames]


    def interpret_results(self, results, cutoff=0.5):
        # Assuming arg: results is something like a list of tuples
        # of the form ((float)timestamp_t, (float)APIScore_t)
        # where APIScore_t is the score given by classify_frames()
        # to each frame_t fed through the API, normalized to be between [0,1].

        # Also assuming "endtime" is included in settings.

        return timestamps   # where each timestamp is a tuple of start
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
        [Worker.make_clip(timestamp, self.video_path)
         for timestamp in timestamps]


    def kill(self):
        quit()
