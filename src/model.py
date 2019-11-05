class Job:

    "Model - data logic"

    def __init__(self, settings):
        self.video_path = settings.video_path
        self.settings = settings.settings


    def doTheJob(self):
        data = self.classify_frames()
        results = self.interpret_results(data)
        save_clips(results)


    def get_frames(self):
        return 0  # do whatever to get frames from vid as specific times using self.settings


    def classify_frames(self):
        frames = self.get_frames()
        # use multiprocessing on loop in list comprehension below
        return [Worker.classify_img(frame) for frame in frames]


    def interpret_results(self, results):
        # Assuming arg: results is something like a list of tuples
        # of the form ((float)timestamp_t, (float)APIScore_t)

        return timestamps  # where each timestamp is a tuple of start time and end time


    def save_clips(self, timestamps):
        # use multiprocessing here
        [Worker.make_clip(timestamp, self.video_path)
         for timestamp in timestamps]


    def kill(self):
        quit()
