import cv2
import numpy as np
from PIL import Image
from imageai.Prediction import ImagePrediction


class Worker:

    "Controller - data requests"

    def __init__(self):
        return

    def classify_img(self, img):
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

# path = 'test/sampleImage/rainbow.jpg'
# img = Image.open(path)
# arr = np.array(img)
# print(img)
# result = Worker().classify_img(img)
# print(result)
