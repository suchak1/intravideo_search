# -*- coding: utf-8 -*-
import cv2
from PIL import Image, ImageChops
import os
import sys
import pytest
import torch
import numpy as np
import pytest_check as check
sys.path.append('src')
sys.path.append('utils')
from build_vocab import Vocabulary
from view import *  # nopep8
from model import *  # nopep8
from seer_model import *

example_parameters1 = {
    'settings': {
        'conf': .9,
        'poll': 5,
        'anti': 5,
        'search': ["dog"],
        'runtime': 5.0
    },
    'video': 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
}

example_job1 = Job(example_parameters1)

example_parameters2 = {
    'settings': {
        'conf': .9,
        'poll': 4,
        'anti': 5,
        'search': ["rabbit"],
        'runtime': 5.0
    },
    'video': 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
}

example_job2 = Job(example_parameters2)

example_parameters3 = {
    'settings': {
        'conf': .9,
        'poll': 1,
        'anti': 3,
        'search': ["rock"],
        'runtime': 5.0
    },
    'video': 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
}

example_job3 = Job(example_parameters3)

example_parameters4 = {
    'settings': {
        'conf': .9,
        'poll': 8,
        'anti': 6,
        'search': ["water"],
        'runtime': 25.0
    },
    'video': 'test/sampleVideo/SampleVideoNature.mp4'
}

example_job4 = Job(example_parameters4)

def test_save_clips():
    timestamps1 = [0, 5]
    timestamps2 = [4, 5]
    timestamps3 = [-1, 5]
    timestamps4 = [10, 5]
    timestamps5 = [1, -5]
    timestamps6 = [1, 1]

    check.is_false(example_job1.save_clips([]))

    with pytest.raises(Exception):
        example_job1.save_clips([timestamps3])
        example_job1.save_clips([timestamps4])
        example_job1.save_clips([timestamps5])
        example_job1.save_clips([timestamps6])

    check.is_true(example_job1.save_clips([timestamps1]))
    check.is_true(example_job1.save_clips([timestamps1, timestamps2]))
    path = os.path.splitext(example_job1.video_path)
    # form of filenames updated to match implementation
    check.is_true(
        os.path.isfile(
            path[0] + '_subclip(' + str(timestamps1[0]) + ',' + str(timestamps1[1]) + ')' + path[1]))
    check.is_true(
        os.path.isfile(
            path[0] + '_subclip(' + str(timestamps2[0]) + ',' + str(timestamps2[1]) + ')' + path[1]))


def test_classify_frames():
    frame_list1 = example_job2.classify_frames()
    frame_list = example_job1.classify_frames()
    check.equal(frame_list1[0][1], 0)
    check.less(frame_list1[0][0], 0.7)
    check.not_equal(frame_list1[1][1], 5)
    check.greater(frame_list1[1][0], 0.7)

    check.equal(frame_list[0][1], 0)
    check.less(frame_list[0][0], 0.7)
    check.not_equal(frame_list[1][1], 4)
    check.greater(frame_list[1][0], 0.7)

def test_score():
    j = Job(example_parameters1)
    api_results1 = {'dog': 0.9, 'cat': 0.7}
    api_results2 = {'cat': 0.7}
    check.equal(j.score(api_results1), 0.9)
    check.equal(j.score(api_results2), 0)
    with pytest.raises(Exception):
        j.score('a string')


def test_job_constructor():
    j = Job({'settings': {'conf': .9, 'poll': 5, 'anti': 5, 'search': ['dog'], 'runtime': 100.0},
             'video': 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'})
    check.equal(j.video_path, 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(j.settings, {'conf': .9, 'poll': 5, 'anti': 5, 'search': ['dog'], 'runtime': 100.0})
    # redundant tests removed from milestone 3a comments
    # runtime key added to test dict as per new specs of settings

def test_interpret_results_null_input():
    job = Job(example_parameters1)
    results = None
    with pytest.raises(Exception):
        ret = job.interpret_results(results)
        assert(isinstance(ret, type(None)))


def test_interpret_results_negative_time():
    job = Job(example_parameters1)
    results = [(-2.0, 0.1)]
    with pytest.raises(Exception):
        job.interpret_results(results)


def test_interpret_results_negative_score():
    job = Job(example_parameters1)
    results = [(3.0, -0.5)]
    with pytest.raises(Exception):
        job.interpret_results(results)


def test_interpret_results_unnormalized_score():
    job = Job(example_parameters1)
    resultsNonNorm = [(3.0, 1.2)]
    with pytest.raises(Exception):
        job.interpret_results(resultsNonNorm)


def test_interpret_results_duplicate_times():
    job = Job(example_parameters1)
    results = [(1.0, 0.1), (1.0, 0.03)]
    with pytest.raises(Exception):
        job.interpret_results(results)


def test_interpret_results_negative_cutoff():
    job = Job(example_parameters1)
    toyResults = [(1.0, 1)]
    with pytest.raises(Exception):
        job.interpret_results(toyResults, cutoff=-0.3)


def test_interpret_results_out_of_order():
    job = Job(example_parameters1)
    results = [(3.0, 0.6), (1.0, 0.03)]
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_mid_clip():
    job = Job(example_parameters1)
    results = [(0.0, 0.1), (10.0, 0.6), (20.0, 0.3), (30.0, 0.2)]
    check.equal(job.interpret_results(results, cutoff=0.5), [(5.0, 15.0)])


def test_interpret_results_spanning_clip():
    job = Job(example_parameters1)
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.01)]

    check.is_true(stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                    [(5.0, 25.0)]))


def test_interpret_results_multiple_seperate_clips():
    job = Job(example_parameters1)
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.1),
               (40.0, 0.7),
               (50.0, 0.8),
               (60.0, 0.01)]
    check.is_true(stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                     [(5.0, 25.0), (35.0, 55.0)]))


def test_interpret_results_from_start():
    job = Job(example_parameters1)
    results = [(1.0, 0.6), (10.0, 0.2), (20.0, 0.1), (30.0, 0.08)]
    #print(job.interpret_results(results, cutoff=0.5))
    #exit(0)
    output = job.interpret_results(results, cutoff=0.5)
    check.is_true(stampListsAreEqual(output,[(0.0, 5.5)]))


def test_interpret_results_from_end():
    job = Job(example_parameters1)
    results = [(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
    job.settings["runtime"] =  40.0
    check.is_true(stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                     [(25.0, 40.0)]))


def test_interpret_results_zero_cutoff():
    job = Job(example_parameters1)
    results = [(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
    job.settings["runtime"] =  40.0
    check.is_true(stampListsAreEqual(job.interpret_results(results, cutoff=0.0),
                                     [(0.0, 40.0)]))


def test_interpret_results_cutoff_morethan_1():
    job = Job(example_parameters1)
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.1),
               (40.0, 0.7),
               (50.0, 0.8),
               (60.0, 0.01)]
    check.is_true(stampListsAreEqual(
        job.interpret_results(results, cutoff=1.1), []))


def stampListsAreEqual(times1, times2):
    if not isinstance(times1, type([])) or \
       not isinstance(times2, type([])) or \
       not (len(times1) == len(times2)):
        return False

    for i in range(len(times1)):
        if not (times1[i] == times2[i]):
            return False

    return True

# helper function to test get_frames()
def areImagesSame(im1, im2):
    arr1 = np.array(im1)
    arr2 = np.array(im2)

    if arr1.shape != arr2.shape:
        return False

    results = []

    for i, x in enumerate(arr1):
        for j, y in enumerate(x):
            for k, z in enumerate(y):
                px_val1 = int(arr1[i][j][k])
                px_val2 = int(arr2[i][j][k])

                # rgb val diff threshold +/-5
                if abs(px_val1 - px_val2) > 10:
                    results.append(0)
                else:
                    results.append(1)

    # make sure 95% of pixels fall within threshold
    return sum(results) / len(results) > 0.95

# add tests for get_frames() based on comments from milestone 3a
# now test with different videos and different settings
# also test was changed to reflect change in get_frames() return value
# from list of Images to list of tuples of Images and timestamps
def test_get_frames_poll_5():
    frames = example_job1.get_frames()
    frames = list(sorted(frames, key=lambda x: x[1]))
    check.equal(len(frames), 2)
    # frame at 0 seconds of sample video
    frame1 = Image.open('test/sampleVideo/settings_poll_5/frame0.jpg')
    # frame at 5 seconds of sample video
    frame2 = Image.open('test/sampleVideo/settings_poll_5/frame1.jpg')
    # these are same images, so should return true
    check.is_true(areImagesSame(frames[0][0], frame1))
    check.is_true(areImagesSame(frames[1][0], frame2))

    # these are diff images, so should return false
    check.is_false(areImagesSame(frames[1][0], frame1))
    check.is_false(areImagesSame(frames[0][0], frame2))

    check.equal(frames[0][1], 0)
    check.equal(frames[1][1], 5)

def test_get_frames_poll_1():
    frames = example_job3.get_frames()
    frames = list(sorted(frames, key=lambda x: x[1]))
    poll = example_job3.settings['poll']
    check.equal(len(frames), 6)
    # check frames against expected frame at each second (because poll = 1)
    for i in range(6):
        path = 'test/sampleVideo/settings_poll_1/frame%d.jpg' % i
        compare_img = Image.open(path)
        # same image, so should return true
        check.is_true(areImagesSame(frames[i][0], compare_img))
        # comparing test image w previous frame, so should be false
        if i != 0:
            check.is_false(areImagesSame(frames[i-1][0], compare_img))
        check.equal(frames[i][1], i * poll)

def test_get_frames_poll_8():
    frames = example_job4.get_frames()
    frames = list(sorted(frames, key=lambda x: x[1]))
    poll = example_job4.settings['poll']
    check.equal(len(frames), 4)
    # check frames against frame at 0,8,16,24 seconds (because poll = 8)
    for i in range(4):
        path = 'test/sampleVideo/settings_poll_8/frame%d.jpg' % i
        compare_img = Image.open(path)
        # same image, so should return true
        check.is_true(areImagesSame(frames[i][0], compare_img))
        # comparing test image w previous frame, so should be false
        if i != 0:
            check.is_false(areImagesSame(frames[i-1][0], compare_img))
        check.equal(frames[i][1], i * poll)

# The following are tests for Seer.
# There are a total of 4 methods in the Seer class, however two are entirley
# internal and are incorporated into the initialization and the captioning
# function, both of which are tested below.
#
# The initialization merely loads up the proper models (sourced from an
# open source repository, so equivalent to an API) and so the only check
# required is to ensure that the relevant attributes were initialized, and
# that they are of the correct API type.
#
# As for the captioning method (tell_us_oh_wise_one,) multiple image types
# and invalid inputs are tested, as is usual for a unit test.

# Device Config. Use GPU if available.
def test_seer_init():
    delphi = Seer()
    check.is_true(isinstance(delphi.encoder, type(EncoderCNN(1))))
    check.is_true(isinstance(delphi.decoder, type(DecoderRNN(1,1,1,1,1))))
    check.is_true(delphi.vocab_path == 'torchdata/vocab.pkl')
    check.is_true(delphi.encoder_path == 'torchdata/encoder-5-3000.pkl')
    check.is_true(delphi.decoder_path == 'torchdata/decoder-5-3000.pkl')
    check.is_true(delphi.embed_size == 256)
    check.is_true(delphi.hidden_size == 512)
    check.is_true(delphi.num_layers == 1)
    check.is_true(isinstance(delphi.vocab, type(Vocabulary())))

def test_seer_tell_us_oh_wise_one_non_image():
    delphi = Seer()
    notanimg = 5
    with pytest.raises(Exception):
        caption = delphi.tell_us_oh_wise_one(notanimg)

def test_seer_tell_us_oh_wise_one_nonetype():
    delphi = Seer()
    nonetype = None
    with pytest.raises(Exception):
        caption = delphi.tell_us_oh_wise_one(nonetype)

def test_seer_tell_us_oh_wise_one_jpg():
    delphi = Seer()
    img = Image.open("test/sampleImage/golden retriever.jpg")
    caption = delphi.tell_us_oh_wise_one(img)
    true_caption = "a dog is sitting on a couch with a frisbee"
    check.is_true(caption == true_caption)

def test_seer_tell_us_oh_wise_one_png():
    delphi = Seer()
    img = Image.open("test/sampleImage/blindside.png")
    caption = delphi.tell_us_oh_wise_one(img)
    true_caption = "a living room with a couch and a television"
    check.is_true(caption == true_caption)

def test_seer_tell_us_oh_wise_one_black_and_white():
    delphi = Seer()
    img = Image.open("test/sampleImage/bandw.jpg")
    caption = delphi.tell_us_oh_wise_one(img)
    true_caption = "a black and white photo of a train station"
    check.is_true(caption == true_caption)

# helper function to test get_from_yt()
def get_vid_duration(path):
    v=cv2.VideoCapture(path)
    fps = v.get(cv2.CAP_PROP_FPS)
    frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count/fps)
    return duration

@pytest.mark.skipif(os.environ.get('CI') == 'true',
                    reason="Travis' IP is prob on a blocklist.")
def test_get_from_yt():
    parameters = {
    'settings': {
        'conf': .9,'poll': 5,'anti': 5,'search': [''],'runtime':100.0},
        'video': ''
    }
    invalid_url1 = 'https://www.youtube.com/watch?v=sVuG2i93notvalid'
    invalid_url2 = 'www.youtube.com'
    invalid_url3 = ''
    invalid_url4 = 'https://vimeo.com/66457941'
    invalid_url5 = 'www.yutub.com/watch?v=dQw4w9WgXQ'
    url1 = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    url2 = 'www.youtube.com/watch?v=fJ9rUzIMcZQ'
    url3 = 'youtube.com/watch?v=VuNIsY6JdUw'
    expected_path1 = './test/Rick Astley - Never Gonna Give You Up (Video).mp4'
    expected_path2 = './test/Queen – Bohemian Rhapsody (Official Video Remastered).mp4'
    expected_path3 = './test/Taylor Swift - You Belong With Me.mp4'
    expected_duration1 = 212 # durations in seconds
    expected_duration2 = 359
    expected_duration3 = 228
    job0 = Job(parameters)
    job0.handle_vid()

    # test valid url1
    parameters['video'] = url1
    job1 = Job(parameters)
    job1.handle_vid()
    # get_from_yet is called in the initialization of job
    # if parameter video is a YouTube URL
    url1_path = job1.video_path
    check.equal(url1_path,expected_path1)
    check.equal(expected_duration1, get_vid_duration(url1_path))

    # test valid url2
    parameters['video'] = url2
    job2 = Job(parameters)
    job2.handle_vid()
    url2_path = job2.video_path
    check.equal(url2_path,expected_path2)
    check.equal(expected_duration2, get_vid_duration(url2_path))

    # test valid url3
    parameters['video'] = url3
    job3 = Job(parameters)
    job3.handle_vid()
    url3_path = job3.video_path
    check.equal(url3_path,expected_path3)
    check.equal(expected_duration3, get_vid_duration(url3_path))

    # test invalid inputs using arbitrary job to access get_from_yt() function
    with pytest.raises(Exception):
        job0.get_from_yt(invalid_url1)
    with pytest.raises(Exception):
        job0.get_from_yt(invalid_url2)
    with pytest.raises(Exception):
        job0.get_from_yt(invalid_url3)
    with pytest.raises(Exception):
        job0.get_from_yt(invalid_url4)
    with pytest.raises(Exception):
        job0.get_from_yt(invalid_url5)
