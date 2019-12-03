import cv2
import filecmp
import os
from moviepy.editor import VideoFileClip
from PIL import Image
from imageai.Prediction import ImagePrediction
import requests


class Worker:

    "Controller - data requests"

    def __init__(self, video_path=None):
        self.video_path = video_path

    def classify_img(self, img):
        # input: Image object to classify
        # output: classification results in dictionary
        # where key is object as a string
        # and value is confidence level scaled 0-100
        if not isinstance(img, Image.Image):
            return None

        model_path = 'src/squeezenet_weights_tf_dim_ordering_tf_kernels.h5'
        model = ImagePrediction()
        model.setModelTypeAsSqueezeNet()
        model.setModelPath(model_path)
        model.loadModel()

        predictions, probabilities = [elem[::-1] for elem in model.predictImage(img, input_type = 'array')]
        results = {}

        for idx, prediction in enumerate(predictions):
            related_words = self.get_related_words(prediction)
            results.update({word: probabilities[idx] for word in related_words})

        return results

    def get_related_words(self, word):
        # input: string / term
        # output: dictionary of related words
        # to be used in classify_img to help classify objs

        # arbitrary number of related words to fetch
        # the higher the number, the more tolerant the classification results
        num = 20

        words = word.split('_')
        extra = words + [' '.join(words)] if len(words) > 1 else words
        query = '+'.join(words)
        response = requests.get('https://api.datamuse.com/words?ml=' + query)
        if not word or not response:
            return {}
        else:
            data = response.json()
        related = set([word['word'] for word in data if 'tags' in word and 'n' in word['tags']][:num])
        related.update(extra)
        return related

    def make_clip(self, timestamp, outputPath=None):
        # Args: timestamp:((int)t0, (int)t1)
        #       path: (string)"path/to/input/video.mp4"
        #       outputPath: (string) "path/to/destination/video.mp4"

        # Check for valid args
        path = self.video_path
        if isinstance(timestamp, type(None)) or isinstance(path, type(None)) \
                                             or isinstance(timestamp[0], type(None)) \
                                             or isinstance(timestamp[1], type(None)):
            raise TypeError("Nonetype in arguments. Naughty naughty.")
        if not os.path.isfile(path):
            raise ValueError("No file at {}".format(path))

        start, end = timestamp
        # For the destination path, use the outputPath given, or else use the
        # default template.
        if isinstance(outputPath, type(None)):
            pathRoot, pathExt = os.path.splitext(path)
            clipPath = pathRoot + "_subclip({},{})".format(start, end) + pathExt
        else:
            clipPath = outputPath

        # After getting the relevant information about the video,
        # ensure that the parameters are properly formatted or otherwise
        # good-to-go and make a sub-clip.
        numFrames, fps, framH, frameW, fourcc = self.get_video_info(path)
        if end > int(numFrames/fps):
            end = int(numFrames/fps)
        delta = end - start
        if delta < 0:
            raise ValueError("Timestamp is out of order! Abort!")
        if delta == 0:
            raise ValueError("There is no interval in this timestamp {}".format(timestamp))
        if int(delta*fps) < 1:
            return ""
        if start < 0 or end < 0:
            raise ValueError("Negative time in the timestamp. That can't be right.")

        # Make that subclip.
        clip = VideoFileClip(path).subclip(start, end)

        # due to multiprocessing, we must give unique names to temp audio files
        audio_path = f'temp-audio({start}_{end}).mp4'

        clip.write_videofile(
            clipPath,
            codec='libx264',
            temp_audiofile=audio_path,
            remove_temp=True,
            audio_codec='aac'
        )

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
