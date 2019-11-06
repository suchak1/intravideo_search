import sys
import pytest
sys.path.append('src')
from controller import *  # nopep8
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2



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
    clipPath = "test/sampleVideo/test.mp4"
    w = Worker()
    timestamp = (1.0, 1.0000001)
    # # TODO:

def test_make_clip_full_video():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    w = Worker()
    timestamp = (0.0, 100000000000.0)
    outVidPath = w.make_clip(timestamp, videoPath)
    assert areVideosAndAreEqual(videoPath, outVidPath)


def test_make_clip_from_mid():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    clipPath = "test/sampleVideo/test.mp4"
    timestamp = (1.0, 3.0)
    ffmpeg_extract_subclip(videoPath, timestamp[0], timestamp[1], targetname=clipPath)
    w = Worker()
    outVidPath = w.make_clip(timestamp, videoPath)
    assert areVideosAndAreEqual(clipPath, outVidPath)

def test_make_clip_from_start():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    clipPath = "test/sampleVideo/test.mp4"
    timestamp = (0.0, 3.0)
    ffmpeg_extract_subclip(videoPath, timestamp[0], timestamp[1], targetname=clipPath)
    w = Worker()
    outVidPath = w.make_clip(timestamp, videoPath)
    assert areVideosAndAreEqual(clipPath, outVidPath)


def test_make_clip_from_end():
    videoPath = "test/sampleVideo/SampleVideo_1280x720_1mb.mp4"
    clipPath = "test/sampleVideo/test.mp4"
    timestamp = (3.0, 1000000.0)
    ffmpeg_extract_subclip(videoPath, timestamp[0], timestamp[1], targetname=clipPath)
    w = Worker()
    outVidPath = w.make_clip(timestamp, videoPath)
    assert areVideosAndAreEqual(clipPath, outVidPath)


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
