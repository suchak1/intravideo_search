# -*- coding: utf-8 -*-

import sys
sys.path.append('src')
from view import *
from model import *  # nopep8


example_parameters1 = {
        'settings': {
            'confidence': .9,
            'poll': 5,
            'anti_classification': 5,
            'search_terms': ["dog"]
            },
        'video_path': '/videos/example_video.mov'
        }

example_job1 = Job(example_parameters1)


def test_save_clips():
    timestamps1 = [0, 5]
    timestamps2 = [4, 5]
    timestamps3 = [-1, 5]
    timestamps4 = [10, 5]
    timestamps5 = [1, -5]
    assert not example_job1.save_clips([])
    assert not example_job1.save_clips([timestamps3])
    assert not example_job1.save_clips([timestamps4])
    assert not example_job1.save_clips([timestamps5])
    assert example_job1.save_clips([timestamps1])
    assert example_job1.save_clips([timestamps1, timestamps2])
    path = os.path.splitext(example_job1.settings['video_path'])
    assert os.path.isfile(path[0] + '_' + str(timestamps1[0]) + '_' + str(timestamps1[1]) + path[1])
    assert os.path.isfile(path[0] + '_' + str(timestamps2[0]) + '_' + str(timestamps2[1]) + path[1])


def test_job_constructor():
    g = GUI()
    g.set_settings({'conf':.9, 'poll':5, 'anti':5, 'search':['dog']},
                    'test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    j = Job(g)
    assert getattr(j, 'video_path') == 'test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
    assert getattr(j, 'settings') == {'conf':.9, 'poll':5, 'anti':5, 'search':['dog']}
    assert callable(getattr(j, 'get_frames')) == True
    assert callable(getattr(j, 'classify_frames')) == True
    assert callable(getattr(j, 'interpret_results')) == True
    assert callable(getattr(j, 'save_clips')) == True
    assert callable(getattr(j, 'kill')) == True
