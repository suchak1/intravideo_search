import cv2


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
        clipPath = path + "_subclip({},{})".format(timestamp[0], timestamp[1])
        ffmpeg_extract_subclip(path, timestamp[0], timestamp[1], targetname=clipPath)
        return clipPath  # clip path
