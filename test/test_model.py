# -*- coding: utf-8 -*-
import cv2
from PIL import Image, ImageChops
import os
import sys
import pytest
import pytest_check as check
sys.path.append('src')
from view import *  # nopep8
from model import *  # nopep8

example_parameters1 = {
    'settings': {
        'conf': .9,
        'poll': 5,
        'anti': 5,
        'search': ["dog"],
        'runtime':100.0
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
        'runtime':100.0
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
        'runtime':100.0
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
        'runtime':100.0
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
    check.equal(frame_list1[0][0], 0)
    check.is_greater(frame_list1[0][1], 0.7)
    check.equal(frame_list1[1][0], 5)
    check.is_greater(frame_list1[1][1], 0.7)

    check.equal(frame_list[0][0], 0)
    check.is_less(frame_list[0][1], 0.7)
    check.equal(frame_list[1][0], 4)
    check.is_less(frame_list[1][1], 0.7)

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
    return ImageChops.difference(im1, im2).getbbox() is None

# add tests for get_frames() based on comments from milestone 3a
# now test with different videos and different settings
# also test was changed to reflect change in get_frames() return value
# from list of Images to list of tuples of Images and timestamps
def test_get_frames_poll_5():
    frames = example_job1.get_frames()
    check.equal(len(frames), 2)
    # frame at 0 seconds of sample video
    frame1 = Image.open('test/sampleVideo/settings_poll_5/frame0.jpg')
    # frame at 5 seconds of sample video
    frame2 = Image.open('test/sampleVideo/settings_poll_5/frame1.jpg')
    check.is_true(areImagesSame(frames[0][0], frame1))
    check.is_true(areImagesSame(frames[1][0], frame2))
    check.equal(frames[0][1], 0)
    check.equal(frames[1][1], 5)

def test_get_frames_poll_1():
    frames = example_job3.get_frames()
    poll = example_job3.settings['poll']
    check.equal(len(frames), 6)
    # check frames against expected frame at each second (because poll = 1)
    for i in range(6):
        path = 'test/sampleVideo/settings_poll_1/frame%d.jpg' % i
        compare_img = Image.open(path)
        check.is_true(areImagesSame(frames[i][0], compare_img))
        check.equal(frames[i][1],i*poll)

def test_get_frames_poll_8():
    frames = example_job4.get_frames()
    poll = example_job4.settings['poll']
    check.equal(len(frames), 4)
    # check frames against frame at 0,8,16,24 seconds (because poll = 8)
    for i in range(4):
        path = 'test/sampleVideo/settings_poll_8/frame%d.jpg' % i
        compare_img = Image.open(path)
        check.is_true(areImagesSame(frames[i][0], compare_img))
        check.equal(frames[i][1],i*poll)
