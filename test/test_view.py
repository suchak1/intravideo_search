# -*- coding: utf-8 -*-
import tkinter as tk
import sys
import pytest
import pytest_check as check
sys.path.append('src')
from view import *  # nopep8
from model import *  # nopep8


def test_constructor():

    # Currently, when the GUI object is created, we are only allowing
    # the default values to be used.

    # test default constructor with no paramters
    test_gui = GUI()
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {'conf': .9,
                                    'poll': 5, 'anti': 5, 'search': [""]})
    check.is_none(test_gui.job)


def test_set_settings():
    path = 'here/is/a/path'
    notapath = 52

    view = GUI()

    set1 = {'conf': 0.9, 'poll': 5, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    check.is_true(view.set_settings(set1, path))
    check.is_false(view.set_settings(set1, notapath))

    set2 = {'conf': 0.1, 'poll': 2, 'anti': 8,
            'search': ['car']}  # should be true
    check.is_true(view.set_settings(set2, path))
    check.is_false(view.set_settings(set2, notapath))

    set3 = {'conf': 0, 'poll': 5, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    check.is_true(view.set_settings(set3, path))
    check.is_false(view.set_settings(set3, notapath))

    # should be false, conf is negative
    set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}
    check.is_false(view.set_settings(set4, path))
    check.is_false(view.set_settings(set4, notapath))

    set5 = {'conf': 1.0, 'poll': 5, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    check.is_true(view.set_settings(set5, path))
    check.is_false(view.set_settings(set5, notapath))

    set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [
        'dog', 'pet']}  # should be false, conf is >1
    check.is_false(view.set_settings(set6, path))
    check.is_false(view.set_settings(set6, notapath))

    set7 = {'conf': 0.9, 'poll': 0, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    check.is_true(view.set_settings(set7, path))
    check.is_false(view.set_settings(set7, notapath))

    set8 = {'conf': 1.1, 'poll': -1, 'anti': 5,
            'search': ['dog', 'pet']}  # should be false, poll is < 0
    check.is_true(view.set_settings(set8, path))
    check.is_false(view.set_settings(set8, notapath))

    set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    check.is_false(view.set_settings(set9, path))
    check.is_false(view.set_settings(set9, notapath))

    set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': [
        'dog', 'pet']}  # should be false, poll is not an integer
    check.is_true(view.set_settings(set10, path))
    check.is_false(view.set_settings(set10, notapath))

    set11 = {'conf': 1.1, 'poll': 5, 'anti': 0,
             'search': ['dog', 'pet']}  # should be true
    check.is_false(view.set_settings(set11, path))
    check.is_false(view.set_settings(set11, notapath))

    set12 = {'conf': 1.1, 'poll': 5, 'anti': -1,
             'search': ['dog', 'pet']}  # should be false, anti is < 0
    check.is_true(view.set_settings(set12, path))
    check.is_false(view.set_settings(set12, notapath))

    set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000,
             'search': ['dog', 'pet']}  # should be true
    check.is_true(view.set_settings(set13, path))
    check.is_false(view.set_settings(set13, notapath))

    set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': [
        'dog', 'pet']}  # should be false, anti is not an integer
    check.is_false(view.set_settings(set14, path))
    check.is_false(view.set_settings(set14, notapath))

    set15 = {'conf': 1.1, 'poll': 5, 'anti': 5,
             'search': ['dog', 'pet', '50']}  # should be true
    check.is_true(view.set_settings(set15, path))
    check.is_false(view.set_settings(set15, notapath))

    # should be false, no search terms
    set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []}
    check.is_false(view.set_settings(set16, path))
    check.is_false(view.set_settings(set16, notapath))

    # should be false, one value is not a string
    set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']}
    check.is_false(view.set_settings(set17, path))
    check.is_false(view.set_settings(set17, notapath))

    # should be true, even if out of order
    set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5}
    check.is_true(view.set_settings(set18, path))
    check.is_false(view.set_settings(set18, notapath))

    set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}  # should be false
    check.is_false(view.set_settings(set19, path))
    check.is_false(view.set_settings(set19, notapath))

    set20 = {'conf': 1.1, 'anti': 5, 'search': [
        'dog', 'pet']}  # should be false
    check.is_false(view.set_settings(set20, path))
    check.is_false(view.set_settings(set20, notapath))

    set21 = {'conf': 1.1, 'poll': 5, 'search': [
        'dog', 'pet']}  # should be false
    check.is_false(view.set_settings(set21, path))
    check.is_false(view.set_settings(set21, notapath))

    set22 = {'conf': 1.1, 'poll': 5, 'anti': 5}  # should be false
    check.is_false(view.set_settings(set22, path))
    check.is_false(view.set_settings(set22, notapath))

    set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': [
        'dog', 'pet'], 'video': 'path/to/video'}  # should be false, extra key
    check.is_false(view.set_settings(set23, path))
    check.is_false(view.set_settings(set23, notapath))

    set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': [
        'dog', 'pet'], 'x': 0}  # should be false
    check.is_false(view.set_settings(set24, path))
    check.is_false(view.set_settings(set24, notapath))


def test_get_settings():
    """
            Assumption: If set_settings fails, the default values are set for all of the parameters
    """

    path = 'here/is/a/path'
    notapath = 52

    view = GUI()
    default = {"video": '', "settings": {'conf': 0.9,
                                         'poll': 5, 'anti': 5, 'search': []}}  # default settings
    check.equal(view.get_settings(), default)  # should be the default

    set1 = {'conf': 0.9, 'poll': 5, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    d1 = {"video": 'here/is/a/path', "settings": {'conf': 0.9,
                                                  'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}
    view.set_settings(set1, path)
    check.equal(view.get_settings(), d1)
    view.set_settings(set1, notapath)
    check.equal(view.get_settings(), default)

    set2 = {'conf': 0.1, 'poll': 2, 'anti': 8,
            'search': ['car']}  # should be true
    d2 = {"video": 'here/is/a/path', "settings": {'conf': 0.1,
                                                  'poll': 2, 'anti': 8, 'search': ['car']}}
    view.set_settings(set2, path)
    check.equal(view.get_settings(), d2)
    view.set_settings(set2, notapath)
    check.equal(view.get_settings(), default)

    set3 = {'conf': 0, 'poll': 5, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    d3 = {"video": 'here/is/a/path', "settings": {'conf': 0,
                                                  'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}
    view.set_settings(set3, path)
    check.equal(view.get_settings(), d3)
    view.set_settings(set3, notapath)
    check.equal(view.get_settings(), default)

    # should be false, conf is negative
    set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}
    view.set_settings(set4, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set4, notapath)
    check.equal(view.get_settings(), default)

    set5 = {'conf': 1.0, 'poll': 5, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    d5 = {"video": 'here/is/a/path', "settings": set5}
    view.set_settings(set5, path)
    check.equal(view.get_settings(), d5)
    view.set_settings(set5, notapath)
    check.equal(view.get_settings(), default)

    set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [
        'dog', 'pet']}  # should be false, conf is >1
    view.set_settings(set6, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set6, notapath)
    check.equal(view.get_settings(), default)

    set7 = {'conf': 0.9, 'poll': 0, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    d7 = {"video": 'here/is/a/path', "settings": set7}
    view.set_settings(set7, path)
    check.equal(view.get_settings(), d7)
    view.set_settings(set7, notapath)
    check.equal(view.get_settings(), default)

    set8 = {'conf': 1.1, 'poll': -1, 'anti': 5,
            'search': ['dog', 'pet']}  # should be false, poll is < 0
    view.set_settings(set8, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set8, notapath)
    check.equal(view.get_settings(), default)

    set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5,
            'search': ['dog', 'pet']}  # should be true
    d9 = {"video": 'here/is/a/path', "settings": set9}
    view.set_settings(set9, path)
    check.equal(view.get_settings(), d9)
    view.set_settings(set9, notapath)
    check.equal(view.get_settings(), default)

    set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': [
        'dog', 'pet']}  # should be false, poll is not an integer
    view.set_settings(set10, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set10, notapath)
    check.equal(view.get_settings(), default)

    set11 = {'conf': 1.1, 'poll': 5, 'anti': 0,
             'search': ['dog', 'pet']}  # should be true
    d11 = {"video": 'here/is/a/path', "settings": set11}
    view.set_settings(set11, path)
    check.equal(view.get_settings(), d11)
    view.set_settings(set11, notapath)
    check.equal(view.get_settings(), default)

    set12 = {'conf': 1.1, 'poll': 5, 'anti': -1,
             'search': ['dog', 'pet']}  # should be false, anti is < 0
    view.set_settings(set12, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set12, notapath)
    check.equal(view.get_settings(), default)

    set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000,
             'search': ['dog', 'pet']}  # should be true
    d13 = {"video": 'here/is/a/path', "settings": set13}
    view.set_settings(set13, path)
    check.equal(view.get_settings(), d13)
    view.set_settings(set13, notapath)
    check.equal(view.get_settings(), default)

    set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': [
        'dog', 'pet']}  # should be false, anti is not an integer
    view.set_settings(set14, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set14, notapath)
    check.equal(view.get_settings(), default)

    set15 = {'conf': 1.1, 'poll': 5, 'anti': 5,
             'search': ['dog', 'pet', '50']}  # should be true
    d15 = {"video": 'here/is/a/path', "settings": set15}
    view.set_settings(set15, path)
    check.equal(view.get_settings(), d15)
    view.set_settings(set15, notapath)
    check.equal(view.get_settings(), default)

    # should be false, no search terms
    set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []}
    view.set_settings(set16, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set16, notapath)
    check.equal(view.get_settings(), default)

    # should be false, one value is not a string
    set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']}
    view.set_settings(set17, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set17, notapath)
    check.equal(view.get_settings(), default)

    # should be true, even if out of order
    set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5}
    d18 = {"video": 'here/is/a/path', "settings": set18}
    view.set_settings(set18, path)
    check.equal(view.get_settings(), d18)
    view.set_settings(set18, notapath)
    check.equal(view.get_settings(), default)

    set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}  # should be false
    view.set_settings(set19, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set19, notapath)
    check.equal(view.get_settings(), default)

    set20 = {'conf': 1.1, 'anti': 5, 'search': [
        'dog', 'pet']}  # should be false
    view.set_settings(set20, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set20, notapath)
    check.equal(view.get_settings(), default)

    set21 = {'conf': 1.1, 'poll': 5, 'search': [
        'dog', 'pet']}  # should be false
    view.set_settings(set21, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set21, notapath)
    check.equal(view.get_settings(), default)

    set22 = {'conf': 1.1, 'poll': 5, 'anti': 5}  # should be false
    view.set_settings(set22, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set22, notapath)
    check.equal(view.get_settings(), default)

    set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': [
        'dog', 'pet'], 'video': 'path/to/video'}  # should be false, extra key
    view.set_settings(set23, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set23, notapath)
    check.equal(view.get_settings(), default)

    set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': [
        'dog', 'pet'], 'x': 0}  # should be false
    view.set_settings(set24, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set24, notapath)
    check.equal(view.get_settings(), default)


def test_start():
    view = GUI()
    check.is_true(view.start_job())


def test_kill():
    view = GUI()
    check.is_true(view.kill_job())


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
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {'conf': .9,
                                    'poll': 5, 'anti': 5, 'search': [""]})
    check.is_none(test_gui.job)

    # change the parameters to some valid input that a user would use
    test_gui.video_path = '~/Desktop/test.mp4'
    test_gui.set_settings({'conf': .5, 'poll': 3, 'anti': 1, 'search': [
                          "child"]}, test_gui.video_path)
    test_job1 = Job(test_gui.get_settings())
    test_gui.job = test_job1
    # assert that these changes have gone through
    check.equal(test_gui.video_path, '~/Desktop/test.mp4')
    check.equal(test_gui.settings, {'settings': {'conf': .5, 'poll': 3, 'anti': 1, 'search': [
        "child"]}, 'video': '~/Desktop/test.mp4'})
    # assert test_gui.job check.equal() test_job1

    test_gui.render()

    # change the parameters to another valid input that a user would use
    test_gui.video_path = '../folder2/video.mp4'
    test_gui.set_settings({'conf': 0.2, 'poll': 0, 'anti': 0, 'search': [
                          "child, kid, ball"]}, test_gui.video_path)
    test_job1 = Job({'settings': test_gui.settings, 'video': test_gui.video_path})
    test_gui.job = test_job1
    # assert that these changes have gone through
    check.equal(test_gui.video_path, '../folder2/video.mp4')
    check.equal(test_gui.settings, {'settings' : {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': [
        "child, kid, ball"]}, 'video': '../folder2/video.mp4'})
    check.equal(test_gui.job, test_job1)

    test_gui.render()

    # change the video path to a very very long video path.
    # Keep the rest of the parameters the same
    test_gui.video_path = '../folder2/video/folder2/folder7/New Folder/Killa/destroy/superlongfoldernamethatshouldnotbeallowed/testfolder/youcouldntfindmecouldyou.mp4'
    check.equal(test_gui.video_path, '../folder2/video/folder2/folder7/New Folder/Killa/destroy/superlongfoldernamethatshouldnotbeallowed/testfolder/youcouldntfindmecouldyou.mp4')
    test_gui.set_settings(test_gui.settings, test_gui.video_path)
    # make sure the other two parameters have not changed
    check.equal(test_gui.settings, {'settings' : {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': [
        "child, kid, ball"]}, 'video': test_gui.video_path})
    check.equal(test_gui.job, test_job1)

    test_gui.render()

    # change the video path to an empty one, can raise an error or allow this input.
    # the other inputs should remain the same
    test_gui.video_path = ''
    # reset the settings to remove the path
    test_gui.settings = {'conf': 0.2, 'poll': 0,
                         'anti': 0, 'search': ["child, kid, ball"]}
    test_gui.set_settings(test_gui.settings, test_gui.video_path)
    # make sure the correct parameters have changed
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {'settings' : {'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"]}, 'video': ''})
    check.equal(test_gui.job, test_job1)

    test_gui.render()

    # change video path to an invalid value or type
    # the point of this test to make sure the GUI visually throws an error message
    # Because these types of errors will be caught by the logic unit tests,
    test_gui.set_settings({'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"]}, 2)

    # make sure that the parameters have not changed from the false input
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {
        'conf': 0.2, 'poll': 0, 'anti': 0, 'search': ["child, kid, ball"]})
    check.equal(test_gui.job, test_job1)

    # Here, we will start testing more levels of the settings parameter in specific.
    # Valid inputs for settings should not throw a GUI error message
    # Incorrect inputs for settings should throw a GUI error message when rendered.

    # create a clean new GUI object
    test_gui2 = GUI()

    # change the video_path to a normal one, make sure GUI does not throw an error
    test_gui2.video_path = '~/Documents/downloadedvideo.mp4'
    test_gui2.settings = {'conf': .75, 'poll': 571,
                          'anti': 462, 'search': ["comptuter"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # make sure that these parameters have been appropriately changed
    check.equal(test_gui2.video_path, '~/Documents/downloadedvideo.mp4')
    check.equal(test_gui2.settings, {'conf': .9, 'poll': 5, 'anti': 5, 'search': [
        ""], 'path': '~/Documents/downloadedvideo.mp4'})
    check.is_none(test_gui2.job)

    # change the settings used so there are some invalid values (negative settings)
    test_gui2.settings = {'conf': -10, 'poll': -
                          1, 'anti': -5, 'search': ["uhhhh"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # assert that these changes do not go through and the previous values remain
    check.equal(test_gui2.video_path, '~/Documents/downloadedvideo.mp4')
    check.equal(test_gui2.settings, {'conf': .9, 'poll': 5, 'anti': 5, 'search': [
        ""], 'path': '~/Documents/downloadedvideo.mp4'})
    check.is_none(test_gui.job)

    test_gui2.render()

    # change the settings to the wrong type
    test_gui2.settings = {'conf': 'hello', 'poll': 'nice',
                          'anti': 'should not work', 'search': ["seach term"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # assert that these changes do not go through and the previous values remain
    check.equal(test_gui2.video_path, '~/Documents/downloadedvideo.mp4')
    check.equal(test_gui2.settings, {'conf': .9, 'poll': 5, 'anti': 5, 'search': [
        ""], 'path': '~/Documents/downloadedvideo.mp4'})
    check.is_none(test_gui.job)

    test_gui2.render()

    # starting tests for changing around the third parameter, job.

    # create a new GUI object
    test_gui3 = GUI()

    # change the video_path to something other an empty
    test_gui3.video_path = '~/Downloads/testingdifferentjobs.mp4'
    test_gui3.set_settings(test_gui3.settings, test_gui3.video_path)
    # make sure the default settings have been invoked into set_settings
    check.equal(test_gui3.video_path, '~/Downloads/testingdifferentjobs.mp4')
    check.equal(test_gui3.settings, {'conf': .9, 'poll': 5, 'anti': 5, 'search': [
        ""], 'path': '~/Downloads/testingdifferentjobs.mp4'})
    check.is_none(test_gui3.job)

    # create a new Job object with the default parameters in the GUI object
    test_job3 = Job({'settings': test_gui3.settings, 'video': test_gui3.video_path})

    # change the value of the GUI's job
    test_gui3.job = test_job3
    # make sure job has changed, but all the other settings stay the same
    check.equal(test_gui3.video_path, '~/Downloads/testingdifferentjobs.mp4')
    check.equal(test_gui3.settings, {'conf': .9, 'poll': 5, 'anti': 5, 'search': [
        ""], 'path': '~/Downloads/testingdifferentjobs.mp4'})
    check.equal(test_gui3.job, test_job3)

    # change the job back to None
    test_gui3.job = None
    # make sure job has changed, but all the other settings stay the same
    check.equal(test_gui3.video_path, '~/Downloads/testingdifferentjobs.mp4')
    check.equal(test_gui3.settings, {'conf': .9, 'poll': 5, 'anti': 5, 'search': [
        ""], 'path': '~/Downloads/testingdifferentjobs.mp4'})
    check.is_none(test_gui3.job)

test_constructor()
test_set_settings()
test_get_settings()
test_render()
