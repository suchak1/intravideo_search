import cv2
import filecmp
import os
from moviepy.editor import VideoFileClip


class Worker:

    "Controller - data requests"

    def __init__(self):
        return

    def classify_img(self, img):
        # make api request
        return  # result

    def classify_img(self, img):
        # make api request
        result = {}
        return result

    def make_clip(self, timestamp, path):
        if isinstance(timestamp, type(None)) or isinstance(path, type(None)) \
                                             or isinstance(timestamp[0], type(None)) \
                                             or isinstance(timestamp[1], type(None)):
            raise TypeError("Nonetype in arguments. Naughty naughty.")

        if not os.path.isfile(path):
            raise ValueError("No file at {}".format(path))

        numFrames, fps, framH, frameW, fourcc = self.getVideoInfo(path)
        clipPath = path[:-4] + "_subclip({},{})".format(timestamp[0], timestamp[1]) + path[-4:]

        if timestamp[1] > int(numFrames/fps):
            timestamp = (timestamp[0], int(numFrames/fps))

        delta = timestamp[1] - timestamp[0]
        if delta < 0:
            raise ValueError("Timestamp is out of order! Abort!")
        if delta == 0:
            raise ValueError("There is no interval in this timestamp {}".format(timestamp))
        if int(delta*fps) < 1:
            return ""
        if timestamp[0] < 0 or timestamp[1] < 0:
            raise ValueError("Negative time in the timestamp. That can't be right.")

        clip = VideoFileClip(path).subclip(timestamp[0], timestamp[1])
        clip.write_videofile(clipPath, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
        return clipPath  # clip path

    def getVideoInfo(self, path):
        video = cv2.VideoCapture(path)
        numFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        frameH = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frameW = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
        return numFrames, fps, frameH, frameW, fourcc
