import cv2
import filecmp
import os
from moviepy.editor import VideoFileClip
from PIL import Image
from imageai.Prediction import ImagePrediction


class Worker:

    "Controller - data requests"

    def __init__(self):
        return

    def classify_img(self, img):
        # input: Image object to classify
        # output: classification results in dictionary
        # where key is object as a string
        # and value is confidence level scaled 0-100
        if not isinstance(img, Image.Image):
            return None

        prediction = ImagePrediction()
        prediction.setModelTypeAsSqueezeNet()
        prediction.setModelPath('src/squeezenet_weights_tf_dim_ordering_tf_kernels.h5')
        prediction.loadModel()

        predictions, probabilities = prediction.predictImage(img, input_type = 'array')
        results = {prediction : probabilities[idx] for idx, prediction in enumerate(predictions)}
        return results

    def get_related_words(self, word):
        # input: string / term
        # output: dictionary of related words
        # to be used in classify_img to help classify objs
        return

    def make_clip(self, timestamp, path, outputPath=None):
        # Args: timestamp:((int)t0, (int)t1)
        #       path: (string)"path/to/input/video.mp4"
        #       outputPath: (string) "path/to/destination/video.mp4"

        # Check for valid args
        if isinstance(timestamp, type(None)) or isinstance(path, type(None)) \
                                             or isinstance(timestamp[0], type(None)) \
                                             or isinstance(timestamp[1], type(None)):
            raise TypeError("Nonetype in arguments. Naughty naughty.")
        if not os.path.isfile(path):
            raise ValueError("No file at {}".format(path))

        # For the destination path, use the outputPath given, or else use the
        # default template.
        if isinstance(outputPath, type(None)):
            pathRoot, pathExt = os.path.splitext(path)
            clipPath = pathRoot + "_subclip({},{})".format(timestamp[0], timestamp[1]) + pathExt
        else:
            clipPath = outputPath

        # After getting the relevant information about the video,
        # ensure that the parameters are properly formatted or otherwise
        # good-to-go and make a sub-clip.
        numFrames, fps, framH, frameW, fourcc = self.get_video_info(path)
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

        # Make that subclip.
        clip = VideoFileClip(path).subclip(timestamp[0], timestamp[1])
        clip.write_videofile(clipPath, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')

        # Return the path to the newly minted clip.
        return clipPath

    def get_video_info(self, path):
        video = cv2.VideoCapture(path)
        numFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        frameH = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frameW = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
        return numFrames, fps, frameH, frameW, fourcc
