from PIL import Image
import os
import sys
import pytest
sys.path.append('src')
from controller import *  # nopep8


def test_constructor():
    w = Worker()
    # Test that the constructor was created correctly and has all the methods
    assert "classify_img" in dir(w)
    assert "make_clip" in dir(w)


def test_classify_img():
    image_dir = '/sampleImage/'
    image_names = ['banana', 'basketball', 'beach', 'box',
                   'car', 'cat', 'cucumber', 'dog', 'person',
                   'rainbow', 'soda', 'sun', 'train', 'waterfall']
    wrong_names = image_names[::-1]
    img_ext = '.jpg'

    # instead of simply using os.getcwd(), we use full_path so that pytest will
    # find the images regardless of where you run pytest
    # (like in test/ as opposed to main dir)

    full_path = os.path.realpath(__file__)
    test_folder = os.path.dirname(full_path)

    w = Worker()
    assert w.classify_img(None) == None

    for idx, name in enumerate(image_names):
        img = Image.open(test_folder + image_dir + name + img_ext)
        # should all be true
        # (that 'banana' is in classification dict for 'banana.jpg' and so on)
        assert name in w.classify_img(img)

        # now let's try assertions that should definitely be wrong
        # (that 'waterfall' is in the classification dict for 'banana.jpg')
        assert wrong_names[idx] not in w.classify(img)
