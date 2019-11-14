import cv2
from PIL import Image
from imageai.Prediction import ImagePrediction


class Worker:

    "Controller - data requests"

    def __init__(self):
        return

    def classify_img(self, img):
        if not isinstance(img, Image.Image):
            return None

        prediction = ImagePrediction()
        prediction.setModelTypeAsSqueezeNet()
        prediction.setModelPath('src/squeezenet_weights_tf_dim_ordering_tf_kernels.h5')
        prediction.loadModel()

        predictions, probabilities = prediction.predictImage(img, input_type = 'array')
        results = {prediction : probabilities[idx] for idx, prediction in enumerate(predictions)}
        return results

    def make_clip(self, timestamp, path):
        # using timestamp[0] (start time) and timestamp[1] (end time)
        return path  # clip path
