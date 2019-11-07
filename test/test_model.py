# -*- coding: utf-8 -*-

import sys
import pytest
sys.path.append('src')
from view import *
from model import *  # nopep8

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
