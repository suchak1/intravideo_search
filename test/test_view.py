# -*- coding: utf-8 -*-
import sys
import pytest
sys.path.append('src')
from view import *  # nopep8
# from model import 
import tkinter as tk

def test_constructor():

    # Currently, when the GUI object is created, we are only allowing
    # the default values to be used.

    # test default constructor with no paramters
    test_gui = GUI()
    assert test_gui.video_path == ''
    assert test_gui.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""]}
    assert test_gui.job == None

    return 0

def test_set_settings():
	path = 'here/is/a/path'
	notapath = 52


	view = GUI()
  
  assert g.start_job()
  assert g.kill_job()
  
	set1 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set1, path) == True
	assert view.set_settings(set1, notapath) == False

	set2 = {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']} #should be true
	assert view.set_settings(set2, path) == True
	assert view.set_settings(set2, notapath) == False

	set3 = {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set3, path) == True
	assert view.set_settings(set3, notapath) == False

	set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is negative
	assert view.set_settings(set4, path) == False
	assert view.set_settings(set4, notapath) == False

	set5 = {'conf': 1.0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set5, path) == True
	assert view.set_settings(set5, notapath) == False

	set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is >1
	assert view.set_settings(set6, path) == False
	assert view.set_settings(set6, notapath) == False

	set7 = {'conf': 0.9, 'poll': 0, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set7, path) == True
	assert view.set_settings(set7, notapath) == False

	set8 = {'conf': 1.1, 'poll': -1, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is < 0
	assert view.set_settings(set8, path) == True
	assert view.set_settings(set8, notapath) == False

	set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set9, path) == False
	assert view.set_settings(set9, notapath) == False

	set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is not an integer
	assert view.set_settings(set10, path) == True
	assert view.set_settings(set10, notapath) == False

	set11 = {'conf': 1.1, 'poll': 5, 'anti': 0, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set11, path) == False
	assert view.set_settings(set11, notapath) == False

	set12 = {'conf': 1.1, 'poll': 5, 'anti': -1, 'search': ['dog', 'pet']} #should be false, anti is < 0
	assert view.set_settings(set12, path) == True
	assert view.set_settings(set12, notapath) == False

	set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set13, path) == True
	assert view.set_settings(set13, notapath) == False

	set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': ['dog', 'pet']} #should be false, anti is not an integer
	assert view.set_settings(set14, path) == False
	assert view.set_settings(set14, notapath) == False

	set15 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet', '50']} #should be true
	assert view.set_settings(set15, path) == True
	assert view.set_settings(set15, notapath) == False

	set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []} #should be false, no search terms
	assert view.set_settings(set16, path) == False
	assert view.set_settings(set16, notapath) == False

	set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']} #should be false, one value is not a string
	assert view.set_settings(set17, path) == False
	assert view.set_settings(set17, notapath) == False

	set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5} #should be true, even if out of order
	assert view.set_settings(set18, path) == True
	assert view.set_settings(set18, notapath) == False

	set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	assert view.set_settings(set19, path) == False
	assert view.set_settings(set19, notapath) == False

	set20 = {'conf': 1.1, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	assert view.set_settings(set20, path) == False
	assert view.set_settings(set20, notapath) == False

	set21 = {'conf': 1.1, 'poll': 5, 'search': ['dog', 'pet']} #should be false
	assert view.set_settings(set21, path) == False
	assert view.set_settings(set21, notapath) == False

	set22 = {'conf': 1.1, 'poll': 5, 'anti': 5} #should be false
	assert view.set_settings(set22, path) == False
	assert view.set_settings(set22, notapath) == False

	set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'video': 'path/to/video'} #should be false, extra key
	assert view.set_settings(set23, path) == False
	assert view.set_settings(set23, notapath) == False

	set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'x': 0} #should be false
	assert view.set_settings(set24, path) == False
	assert view.set_settings(set24, notapath) == False



def test_get_settings():
	"""
		Assumption: If set_settings fails, the default values are set for all of the parameters
	"""

	path = 'here/is/a/path'
	notapath = 52

	view = GUI()
	default = {"video": '', "settings": {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': []}} #default settings
	assert view.get_settings() == default #should be the default

	set1 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d1 = {"video": 'here/is/a/path', "settings": {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}
	view.set_settings(set1, path)
	assert view.get_settings() == d1
	view.set_settings(set1, notapath)
	assert view.get_settings() == default

	set2 = {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']} #should be true
	d2 = {"video": 'here/is/a/path', "settings": {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']}}
	view.set_settings(set2, path)
	assert view.get_settings == d2
	view.set_settings(set2, notapath)
	assert view.get_settings() == default

	set3 = {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d3 = {"video": 'here/is/a/path', "settings": {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}
	view.set_settings(set3, path)
	assert view.get_settings() == d3
	view.set_settings(set3, notapath)
	assert view.get_settings() == default

	set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is negative
	view.set_settings(set4, path)
	assert view.get_settings() == default
	view.set_settings(set4, notapath)
	assert view.get_settings() == default

	set5 = {'conf': 1.0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d5 = {"video": 'here/is/a/path', "settings": set5}
	view.set_settings(set5, path)
	assert view.get_settings() == d5
	view.set_settings(set5, notapath)
	assert view.get_settings() == default


	set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is >1
	view.set_settings(set6, path)
	assert view.get_settings() == default
	view.set_settings(set6, notapath)
	assert view.get_settings() == default

	set7 = {'conf': 0.9, 'poll': 0, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d7 = {"video": 'here/is/a/path', "settings": set7}
	view.set_settings(set7, path)
	assert view.get_settings() == d7
	view.set_settings(set7, notapath)
	assert view.get_settings() == default

	set8 = {'conf': 1.1, 'poll': -1, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is < 0
	view.set_settings(set8, path)
	assert view.get_settings() == default
	view.set_settings(set8, notapath)
	assert view.get_settings() == default

	set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d9 = {"video": 'here/is/a/path', "settings": set9}
	view.set_settings(set9, path)
	assert view.get_settings() == d9
	view.set_settings(set9, notapath)
	assert view.get_settings() == default

	set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is not an integer
	view.set_settings(set10, path)
	assert view.get_settings() == default
	view.set_settings(set10, notapath)
	assert view.get_settings() == default

	set11 = {'conf': 1.1, 'poll': 5, 'anti': 0, 'search': ['dog', 'pet']} #should be true
	d11 = {"video": 'here/is/a/path', "settings": set11}
	view.set_settings(set11, path)
	assert view.get_settings() == d11
	view.set_settings(set11, notapath)
	assert view.get_settings() == default

	set12 = {'conf': 1.1, 'poll': 5, 'anti': -1, 'search': ['dog', 'pet']} #should be false, anti is < 0
	view.set_settings(set12, path)
	assert view.get_settings() == defaults
	view.set_settings(set12, notapath)
	assert view.get_settings() == default

	set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000, 'search': ['dog', 'pet']} #should be true
	d13 = {"video": 'here/is/a/path', "settings": set13}
	view.set_settings(set13, path)
	assert view.get_settings() == d13
	view.set_settings(set13, notapath)
	assert view.get_settings() == default

	set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': ['dog', 'pet']} #should be false, anti is not an integer
	view.set_settings(set14, path)
	assert view.get_settings() == default
	view.set_settings(set14, notapath)
	assert view.get_settings() == default

	set15 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet', '50']} #should be true
	d15 = {"video": 'here/is/a/path', "settings": set15}
	view.set_settings(set15, path)
	assert view.get_settings() == d15
	view.set_settings(set15, notapath)
	assert view.get_settings() == default

	set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []} #should be false, no search terms
	view.set_settings(set16, path)
	assert view.get_settings() == default
	view.set_settings(set16, notapath)
	assert view.get_settings() == default

	set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']} #should be false, one value is not a string
	view.set_settings(set17, path)
	assert view.get_settings() == default
	view.set_settings(set17, notapath)
	assert view.get_settings() == default

	set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5} #should be true, even if out of order
	d18 = {"video": 'here/is/a/path', "settings": set18}
	view.set_settings(set18, path)
	assert view.get_settings() == d18
	view.set_settings(set18, notapath)
	assert view.get_settings() == default

	set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	view.set_settings(set19, path)
	assert view.get_settings() == default
	view.set_settings(set19, notapath)
	assert view.get_settings() == default

	set20 = {'conf': 1.1, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	view.set_settings(set20, path)
	assert view.get_settings() == default
	view.set_settings(set20, notapath)
	assert view.get_settings() == default

	set21 = {'conf': 1.1, 'poll': 5, 'search': ['dog', 'pet']} #should be false
	view.set_settings(set21, path)
	assert view.get_settings() == default
	view.set_settings(set21, notapath)
	assert view.get_settings() == default

	set22 = {'conf': 1.1, 'poll': 5, 'anti': 5} #should be false
	view.set_settings(set22, path)
	assert view.get_settings() == default
	view.set_settings(set22, notapath)
	assert view.get_settings() == default

	set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'video': 'path/to/video'} #should be false, extra key
	view.set_settings(set23, path)
	assert view.get_settings() == default
	view.set_settings(set23, notapath)
	assert view.get_settings() == default

	set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'x': 0} #should be false
	view.set_settings(set24, path)
	assert view.get_settings() == default
	view.set_settings(set24, notapath)
	assert view.get_settings() == default

def test_render():
    # The theory behind test_render is that the unit tests
    # will test whether render() can put underlying changes
    # of the GUI onto the screen correctly.
    # I will be creating a GUI object, rendering it, leaving it on the screen,
    # then killing it. Then, I will change the underlying paramters
    # then re-render another window.

    # Another side note is that by the point of rendering the window,
    # all the inputs will be valid. This is because the GUI technically
    # limits the users to edit the settings within a valid range. However,
    # invalid inputs will also be included in testing.
    #
    # The majority of invalid input testing will be in set_settings and get_settings.


    # Good inputs (changes in the paratmeters that are valid) are included
    # to test that the GUI does NOT throw an error message when a valid input
    # is given.

    test_gui = GUI()
    assert test_gui.video_path == ''
    assert test_gui.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""]}
    assert test_gui.job == None

    # change the parameters to some valid input that a user would use
    test_gui.video_path = '~/Desktop/test.mp4'
    test_gui.set_settings({'conf': .5, 'poll': 3, 'anti': 1, 'search': ["child"]}, test_gui.video_path)
    test_job1 = Job(test_gui.settings)
    test_gui.job = test_job1
    # assert that these changes have gone through
    assert test_gui.video_path == '~/Desktop/test.mp4'
    assert test_gui.settings == {'conf': .5, 'poll': 3, 'anti': 1, 'search': ["child"], 'path': '~/Desktop/test.mp4'}
    #assert test_gui.job == test_job1

    test_gui.render()

    # change the parameters to another valid input that a user would use
    test_gui.video_path = '../folder2/video.mp4'
    test_gui.set_settings({'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"]}, test_gui.video_path)
    test_job1 = Job(test_gui.settings)
    test_gui.job = test_job1
    # assert that these changes have gone through
    assert test_gui.video_path == '../folder2/video.mp4'
    assert test_gui.settings == {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"], 'path': '../folder2/video.mp4'}
    assert test_gui.job == test_job1

    test_gui.render()

    # change the video path to a very very long video path.
    # Keep the rest of the parameters the same
    test_gui.video_path = '../folder2/video/folder2/folder7/New Folder/Killa/destroy/superlongfoldernamethatshouldnotbeallowed/testfolder/youcouldntfindmecouldyou.mp4'
    assert test_gui.video_path == '../folder2/video/folder2/folder7/New Folder/Killa/destroy/superlongfoldernamethatshouldnotbeallowed/testfolder/youcouldntfindmecouldyou.mp4'
    test_gui.set_settings(test_giu.settings, test_gui.video_path)
    # make sure the other two parameters have not changed
    assert test_gui.settings == {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"], 'path': test_giu.video_path}
    assert test_gui.job == test_job1

    test_gui.render()

    # change the video path to an empty one, can raise an error or allow this input.
    # the other inputs should remain the same
    test_gui.video_path = ''
    # reset the settings to remove the path
    test_gui.settings = {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"]}
    test_gui.set_settings(test_gui.settings, test_gui.video_path)
    # make sure the correct parameters have changed
    assert test_gui.video_path == ''
    assert test_gui.settings == {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"], 'path': ''}
    assert test_gui.job == test_job1

    test_gui.render()

    # change video path to an invalid value or type
    # the point of this test to make sure the GUI visually throws an error message
    # Because these types of errors will be caught by the logic unit tests,
    test_gui.video_path = 2
    test_gui.settings = {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"]}
    test_gui.set_settings(test_giu.settings, test_gui.video_path)

    # make sure that the parameters have not changed from the false input
    assert test_gui.video_path == ''
    assert test_gui.settings == {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"]}
    assert test_gui.job == test_job1

    # Here, we will start testing more levels of the settings parameter in specific.
    # Valid inputs for settings should not throw a GUI error message
    # Incorrect inputs for settings should throw a GUI error message when rendered.

    # create a clean new GUI object
    test_gui2 = GUI()

    # change the video_path to a normal one, make sure GUI does not throw an error
    test_gui2.video_path = '~/Documents/downloadedvideo.mp4'
    test_gui2.settings = {'conf': .75, 'poll': 571, 'anti': 462, 'search': ["comptuter"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # make sure that these parameters have been appropriately changed
    assert test_gui2.video_path == '~/Documents/downloadedvideo.mp4'
    assert test_gui2.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""], 'path': '~/Documents/downloadedvideo.mp4'}
    assert test_gui2.job == None


    # change the settings used so there are some invalid values (negative settings)
    test_gui2.settings = {'conf': -10, 'poll': -1, 'anti': -5, 'search': ["uhhhh"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # assert that these changes do not go through and the previous values remain
    assert test_gui2.video_path == '~/Documents/downloadedvideo.mp4'
    assert test_gui2.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""], 'path': '~/Documents/downloadedvideo.mp4'}
    assert test_gui.job == None

    test_gui2.render()

    # change the settings to the wrong type
    test_gui2.settings = {'conf': 'hello', 'poll': 'nice', 'anti': 'should not work', 'search': ["seach term"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # assert that these changes do not go through and the previous values remain
    assert test_gui2.video_path == '~/Documents/downloadedvideo.mp4'
    assert test_gui2.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""], 'path': '~/Documents/downloadedvideo.mp4'}
    assert test_gui.job == None

    test_gui2.render()

    # starting tests for changing around the third parameter, job.

    #create a new GUI object
    test_gui3 = GUI()

    # change the video_path to something other an empty
    test_gui3.video_path == '~/Downloads/testingdifferentjobs.mp4'
    test_gui3.set_settings(test_gui3.settings, test_giu3.video_path)
    # make sure the default settings have been invoked into set_settings
    assert test_gui3.video_path == '~/Downloads/testingdifferentjobs.mp4'
    assert test_gui3.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""], 'path': '~/Downloads/testingdifferentjobs.mp4'}
    assert test_gui3.job == None

    # create a new Job object with the default parameters in the GUI object
    test_job3 = Job(test_gui3.settings)

    # change the value of the GUI's job
    test_gui3.job = test_job3
    # make sure job has changed, but all the other settings stay the same
    assert test_gui3.video_path == '~/Downloads/testingdifferentjobs.mp4'
    assert test_gui3.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""], 'path': '~/Downloads/testingdifferentjobs.mp4'}
    assert test_gui3.job == test_job3

    # change the job back to None
    test_gui3.job = None
    # make sure job has changed, but all the other settings stay the same
    assert test_gui3.video_path == '~/Downloads/testingdifferentjobs.mp4'
    assert test_gui3.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""], 'path': '~/Downloads/testingdifferentjobs.mp4'}
    assert test_gui3.job == None

    # test_constructor()
    # test_render()
