# -*- coding: utf-8 -*-
from PIL import Image
import os
import sys
import pytest
sys.path.append('src')
from view import *
from model import *  # nopep8
import cv2


example_parameters1 = {
        'settings': {
            'conf': .9,
            'poll': 5,
            'anti': 5,
            'search': ["dog"]
            },
        'video_path': 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
        }

example_job1 = Job(example_parameters1)


def test_save_clips():
    timestamps1 = [0, 5]
    timestamps2 = [4, 5]
    timestamps3 = [-1, 5]
    timestamps4 = [10, 5]
    timestamps5 = [1, -5]
    timestamps6 = [1, 1]

    assert not example_job1.save_clips([])

    with pytest.raises(Exception):
        example_job1.save_clips([timestamps3])
        example_job1.save_clips([timestamps4])
        example_job1.save_clips([timestamps5])
        example_job1.save_clips([timestamps6])

    assert example_job1.save_clips([timestamps1])
    assert example_job1.save_clips([timestamps1, timestamps2])
    path = os.path.splitext(example_job1.settings['video_path'])
    assert os.path.isfile(path[0] + '_' + str(timestamps1[0]) + '_' + str(timestamps1[1]) + path[1])
    assert os.path.isfile(path[0] + '_' + str(timestamps2[0]) + '_' + str(timestamps2[1]) + path[1])


def test_job_constructor():
    j = Job({'settings': {'conf':.9, 'poll':5, 'anti':5, 'search':['dog']},
        'video_path': 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'})
    assert getattr(j, 'video_path') == 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
    assert getattr(j, 'settings') == {'conf':.9, 'poll':5, 'anti':5, 'search':['dog']}
    assert callable(getattr(j, 'get_frames')) == True
    assert callable(getattr(j, 'classify_frames')) == True
    assert callable(getattr(j, 'interpret_results')) == True
    assert callable(getattr(j, 'save_clips')) == True
    assert callable(getattr(j, 'kill')) == True

def test_get_frames():
    g = GUI()
    g.set_settings({'conf':.9, 'poll':5, 'anti':5, 'search':['dog']},
                    'test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    j = Job(g)
    frames = j.get_frames()
    assert len(frames) == 2
    # frame at 0 seconds of sample video
    frame1 = Image.open('test/sampleVideo/frame1.jpg')
    # frame at 5 seconds of sample video
    frame2 = Image.open('test/sampleVideo/frame2.jpg')
    assert frames[0].all() == frame1.all()
    assert frames[1].all() == frame2.all()


def test_interpret_results_null_input():
    job = Job()
    results = None
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_empty_input():
    job = Job()
    results = []
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_negative_time():
    job = Job()
    results =[(-2.0, 0.1)]
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_negative_score():
    job = Job()
    results = [(3.0, -0.5)]
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_unnormalized_score():
    job = Job()
    resultsNonNorm = [(3.0, 1.2)]
    with pytest.raises(Exception):
        job.interpret_results(resultsNonNorm)

def test_interpret_results_duplicate_times():
    job = Job()
    results = [(1.0, 0.1), (1.0, 0.03)]
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_negative_cutoff():
    job = Job()
    toyResults = [(1.0, 1)]
    with pytest.raises(Exception):
        job.interpret_results(toyResults, cutoff= -0.3)

def test_interpret_results_out_of_order():
    job = Job()
    results1 = [(3.0, 0.6), (1.0, 0.03)]
    results2 = [(1.0, 0.03), (3.0, 0.6)]
    times1 = job.interpret_results(results1)
    times2 = job.interpret_results(results2)
    assert stampListsAreEqual(times1, times2)


def test_interpret_results_mid_clip():
    job = Job()
    results = [(0.0, 0.1), (10.0, 0.6), (20.0, 0.3), (30.0, 0.2)]
    assert job.interpret_results(results, cutoff=0.5) == [(5.0, 15.0)]

def test_interpret_results_spanning_clip():
    job = Job()
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.01)]
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5), [(0.5,25.0)])

def test_interpret_results_multiple_seperate_clips():
    job = Job()
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.1),
                                                      (40.0, 0.7),
                                                      (50.0, 0.8),
                                                      (60.0, 0.01)]

    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                                [(5.0, 25.0), (35.0, 55.0)])

def test_interpret_results_from_start():
    job = Job()
    results = [(1.0, 0.6), (10.0, 0.2), (20.0, 0.1), (30.0, 0.08)]
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                                            [(0.0, 5.5)])

def test_interpret_results_from_end():
    job = Job()
    results = [(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
    job.settings = {"endtime", 40.0}
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                                            [(25.0, 40.0)])

def test_interpret_results_zero_cutoff():
    job = Job()
    results = [(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
    job.settings = {"endtime", 40.0}
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.0),
                                                                [(0.0, 40.0)])

def test_interpret_results_cutoff_morethan_1():
    job = Job()
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.1),
                                                      (40.0, 0.7),
                                                      (50.0, 0.8),
                                                      (60.0, 0.01)]
    assert stampListsAreEqual(job.interpret_results(results, cutoff=1.1), [])

def stampListsAreEqual(times1, times2):
    if not isinstance(times1, type([])) or \
       not isinstance(times2, type([])) or \
       not (len(times1) == len(times2)):
       return False

    for i in range(len(times1)):
        if not (times1[i] == times2[i]):
            return False

    return True
