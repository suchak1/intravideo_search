class Job:

    "Model - data logic"

    def __init__(self, settings):
        self.video_path = settings['video_path']
        self.settings = settings['settings']

        data = self.classify_frames()
        results = self.interpret_results(data)
        self.save_clips(results)

    def get_frames(self):
        '''
        return 0  # do whatever to get frames from vid as specific times using self.settings
        '''
        pass

    def classify_frames(self):
        '''
        frames = self.get_frames()
        # use multiprocessing on loop in list comprehension below
        return [Worker.classify_img(frame) for frame in frames]
        '''
        pass

    def interpret_results(self, results):
        '''
        return timestamps  # where each timestamp is a tuple of start time and end time
        '''
        pass

    def save_clips(self, timestamps):
        # use multiprocessing here
        '''
        [Worker.make_clip(timestamp, self.video_path)
         for timestamp in timestamps]
        '''
        pass

    def kill(self):
        quit()
