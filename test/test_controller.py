import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image
import os
import sys
import pytest
import pytest_check as check
import filecmp
sys.path.append('src')
from controller import *  # nopep8


def test_constructor():
    w = Worker()
    # Test that the constructor was created correctly and has all the methods
    check.is_true("classify_img" in dir(w))
    check.is_true("make_clip" in dir(w))


def test_classify_img():
    image_dir = '/sampleImage/'
    # Changes to tests:
    # we changed the images classified due to the limitations of our ML model
    # since the model is only trained on 1000 object categories
    # we will create a helper function in the next iteration
    # to test for semantic simularity and get better search results
    image_names = [
        'banana',
        'basketball',
        'carton',
        'cucumber',
        'fountain',
        'golden_retriever',
        'goldfish',
        'passenger_car',
        'pop_bottle',
        'seashore',
        'space_shuttle',
        'sports_car',
        'suit',
        'tabby',
        'volcano'
    ]
    # Changes to tests:
    # wrong_names is a rotation of original image_names
    # as it is unlikely that basketball
    # will be in the classification dict for banana and so on
    wrong_names = image_names[1:] + image_names[:1]
    img_ext = '.jpg'

    # instead of simply using os.getcwd(), we use full_path so that pytest will
    # find the images regardless of where you run pytest
    # (like in test/ as opposed to main dir)

    full_path = os.path.realpath(__file__)
    test_folder = os.path.dirname(full_path)

    w = Worker()
    check.is_none(w.classify_img(None))

    for idx, name in enumerate(image_names):
        img = Image.open(test_folder + image_dir + name + img_ext)
        # should all be true
        # (that 'banana' is in classification dict for 'banana.jpg' and so on)
        check.is_in(name, w.classify_img(img))

        # now let's try assertions that should definitely be wrong
        # (that 'volcano' is in the classification dict for 'banana.jpg')
        check.is_not_in(wrong_names[idx], w.classify_img(img))


def test_get_related_words():
    w = Worker()
    check.equal({}, w.get_related_words(''))
    check.is_in('plantain', w.get_related_words("banana"))
    check.is_in('nba', w.get_related_words("basketball"))
    check.is_in('box', w.get_related_words("carton"))
    check.is_in('zucchini', w.get_related_words("cucumber"))
    check.is_in('waterfall', w.get_related_words("fountain"))
    check.is_in('dog', w.get_related_words("golden retriever"))
    check.is_in('carp', w.get_related_words("goldfish"))
    check.is_in('coach', w.get_related_words("passenger car"))
    check.is_in('soda', w.get_related_words("pop bottle"))
    check.is_in('beach', w.get_related_words("seashore"))
    check.is_in('spaceship', w.get_related_words("space shuttle"))
    check.is_in('roadster', w.get_related_words("sports car"))
    check.is_in('tuxedo', w.get_related_words("suit"))
    check.is_in('cat', w.get_related_words("tabby"))
    check.is_in('lava', w.get_related_words("volcano"))


def test_make_clip_negative_time():
    w = Worker()
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    timestamp = (-1.0, 30.0)
    with pytest.raises(Exception):
        w.make_clip(timestamp, videoPath)


def test_make_clip_out_of_order():
    w = Worker()
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    timestamp = (10.0, 5.0)
    with pytest.raises(Exception):
        w.make_clip(timestamp, videoPath)


def test_make_clip_null_input():
    w = Worker()
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    timestamp = None
    with pytest.raises(Exception):
        w.make_clip(timestamp, videoPath)
    with pytest.raises(Exception):
        w.make_clip((0.0, 1.0), None)


def test_make_clip_zero_delta():
    w = Worker()
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    timestamp = (2.0, 2.0)
    with pytest.raises(Exception):
        w.make_clip(timestamp, videoPath)


def test_make_clip_invalid_vidpath():
    w = Worker()
    videoPath = "this/doesntExist.mp4"
    with pytest.raises(Exception):
        w.make_clip((1.0, 2.0), videoPath)


def test_make_clip_no_frames():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    w = Worker()
    timestamp = (1.0, 1.0000001)
    outVidPath = w.make_clip(timestamp, videoPath)
    check.equal(outVidPath, '')


#   For the following test cases, for make_clip(), they now produce the
#   ground truth comparison video clip in a better way. That is the only
#   change.

def test_make_clip_full_video():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    clipPath = "test/sampleVideo/testFull.mp4"
    w = Worker()
    timestamp = (0.0, 100000000000.0)
    clip = VideoFileClip(videoPath).subclip(timestamp[0], 5.0)
    clip.write_videofile(clipPath, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
    outVidPath = w.make_clip(timestamp, videoPath)
    check.is_true(filecmp.cmp(clipPath, outVidPath))


def test_make_clip_from_mid():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    clipPath = "test/sampleVideo/testMid.mp4"
    timestamp = (1.0, 3.0)
    clip = VideoFileClip(videoPath).subclip(timestamp[0], timestamp[1])
    clip.write_videofile(clipPath, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
    w = Worker()
    outVidPath = w.make_clip(timestamp, videoPath)
    check.is_true(filecmp.cmp(clipPath, outVidPath))


def test_make_clip_from_start():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    clipPath = "test/sampleVideo/testStart.mp4"
    timestamp = (0.0, 3.0)
    clip = VideoFileClip(videoPath).subclip(timestamp[0], timestamp[1])
    clip.write_videofile(clipPath, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
    w = Worker()
    outVidPath = w.make_clip(timestamp, videoPath)
    check.is_true(filecmp.cmp(clipPath, outVidPath))


def test_make_clip_from_end():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    clipPath = "test/sampleVideo/testEnd.mp4"
    timestamp = (3.0, 1000000.0)
    clip = VideoFileClip(videoPath).subclip(timestamp[0], 5.0)
    clip.write_videofile(clipPath, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
    w = Worker()
    outVidPath = w.make_clip(timestamp, videoPath)
    check.is_true(filecmp.cmp(clipPath, outVidPath))



def areVideosAndAreEqual(vidPath1, vidPath2):
    outVid = cv2.VideoCapture(vidPath1)
    testVid = cv2.VideoCapture(vidPath2)
    if not isinstance(testVid, type(cv2.VideoCapture())):
        return False
    if not isinstance(outVid, type(cv2.VideoCapture())):
        return False
    if not videosAreEqual(testVid, outVid):
        return False
    return True


def videosAreEqual(vidCap1, vidCap2):
    while(vidCap1.isOpened() and vidCap2.isOpened()):
        testRet, testFrame = vidCap2.read()
        outRet, outFrame = vidCap1.read()
        if not ((testRet and outRet) or (not testRet and not outRet)):
            return False
        if not testRet:
            break
        if not (testFrame.all() == outFrame.all()):
            return False
    if(testRet or outRet):
        return False
