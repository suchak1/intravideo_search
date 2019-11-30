# -*- coding: utf-8 -*-
import tkinter as tk
import sys
import pytest
import pytest_check as check
sys.path.append('src')
from view import *  # nopep8
from model import *  # nopep8

path = './test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
notapath = 52


#dictionary sets
default = {"video": '', "settings": {'conf': 0.5,
                                         'poll': 5, 'anti': 5, 'runtime': 1, 'search': []}}  # default settings


set1 = {'conf': 0.5, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be true
set2 = {'conf': 0.1, 'poll': 2, 'anti': 8,
            'runtime': 10, 'search': ['car']}  # should be true
set3 = {'conf': 0.0, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be true
set4 = {'conf': -0.1, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']} # should be false, conf is negative
set5 = {'conf': 1.0, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be true
set6 = {'conf': 1.1, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be false, conf is >1
set7 = {'conf': 0.5, 'poll': 0, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be true
set8 = {'conf': 0.5, 'poll': -1, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be false, poll is < 0
set9 = {'conf': 0.5, 'poll': 500000, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be false, poll > 150 - max slider val on gui
set10 = {'conf': 0.5, 'poll': 5.2, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be false, poll is not an integer
set11 = {'conf': 0.5, 'poll': 5, 'anti': 0,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be true
set12 = {'conf': 0.5, 'poll': 5, 'anti': -1,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be false, anti is < 0
set13 = {'conf': 0.5, 'poll': 5, 'anti': 5000000,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be true
set14 = {'conf': 0.5, 'poll': 5, 'anti': 5.2,
            'runtime': 10, 'search': ['dog', 'pet']}  # should be false, anti is not an integer
set15 = {'conf': 0.5, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': ['dog', 'pet', '50']}  # should be true
set16 = {'conf': 0.5, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': []} #should be false, no search terms
set17 = {'conf': 0.5, 'poll': 5, 'anti': 5,
            'runtime': 10, 'search': [84, '84']} # should be false, one value is not a string
set18 = {'search': ['dog', 'pet'], 'poll': 5,
            'conf': 0.5, 'anti': 5, 'runtime': 10} #should be true, even if out of order
set19 = {'poll': 5, 'anti': 5, 'runtime': 10,
            'search': ['dog', 'pet']}  # should be false
set20 = {'conf': 0.5, 'anti': 5, 'runtime': 10,
            'search': ['dog', 'pet']}  # should be false
set21 = {'conf': 0.5, 'poll': 5, 'runtime': 10,
            'search': ['dog', 'pet']}  # should be false
set22 = {'conf': 0.5, 'poll': 5, 'anti': 5, 'runtime': 10}  # should be false
set23 = {'conf': 0.5, 'poll': 5, 'anti': 5, 'runtime': 10,
            'search': ['dog', 'pet'], 'video': 'path/to/video'}  # should be false, extra key
set24 = {'conf': 0.5, 'poll': 5, 'anti': 5, 'runtime': 10,
            'search': ['dog', 'pet'], 'x': 0}  # should be false

def test_constructor():

    # Currently, when the GUI object is created, we are only allowing
    # the default values to be used.

    # test default constructor with no parameters
    test_gui = GUI()
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {'conf': .5,
                                    'poll': 5, 'anti': 5, 'runtime': 1, 'search': []})
    check.is_none(test_gui.job)


def test_set_settings():
    view = GUI()


    check.is_true(view.set_settings(set1, path))
    check.is_false(view.set_settings(set1, notapath))

    check.is_true(view.set_settings(set2, path))
    check.is_false(view.set_settings(set2, notapath))

    check.is_true(view.set_settings(set3, path))
    check.is_false(view.set_settings(set3, notapath))

    check.is_false(view.set_settings(set4, path))
    check.is_false(view.set_settings(set4, notapath))

    check.is_true(view.set_settings(set5, path))
    check.is_false(view.set_settings(set5, notapath))

    check.is_false(view.set_settings(set6, path))
    check.is_false(view.set_settings(set6, notapath))

    check.is_true(view.set_settings(set7, path))
    check.is_false(view.set_settings(set7, notapath))


    check.is_false(view.set_settings(set8, path))
    check.is_false(view.set_settings(set8, notapath))


    check.is_true(view.set_settings(set9, path))
    check.is_false(view.set_settings(set9, notapath))

    check.is_false(view.set_settings(set10, path))
    check.is_false(view.set_settings(set10, notapath))

    check.is_true(view.set_settings(set11, path))
    check.is_false(view.set_settings(set11, notapath))

    check.is_false(view.set_settings(set12, path))
    check.is_false(view.set_settings(set12, notapath))

    check.is_true(view.set_settings(set13, path))
    check.is_false(view.set_settings(set13, notapath))

    check.is_false(view.set_settings(set14, path))
    check.is_false(view.set_settings(set14, notapath))

    check.is_true(view.set_settings(set15, path))
    check.is_false(view.set_settings(set15, notapath))

    check.is_false(view.set_settings(set16, path))
    check.is_false(view.set_settings(set16, notapath))

    check.is_false(view.set_settings(set17, path))
    check.is_false(view.set_settings(set17, notapath))

    check.is_true(view.set_settings(set18, path))
    check.is_false(view.set_settings(set18, notapath))

    check.is_false(view.set_settings(set19, path))
    check.is_false(view.set_settings(set19, notapath))

    check.is_false(view.set_settings(set20, path))
    check.is_false(view.set_settings(set20, notapath))

    check.is_false(view.set_settings(set21, path))
    check.is_false(view.set_settings(set21, notapath))

    check.is_false(view.set_settings(set22, path))
    check.is_false(view.set_settings(set22, notapath))

    check.is_false(view.set_settings(set23, path))
    check.is_false(view.set_settings(set23, notapath))

    check.is_false(view.set_settings(set24, path))
    check.is_false(view.set_settings(set24, notapath))


def test_get_settings():
    """
            Assumption: If set_settings fails, the default values are set for all of the parameters
    """

    view = GUI()
    check.equal(view.get_settings(), default)  # should be the default

    d1 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set1}
    view.set_settings(set1, path)
    check.equal(view.get_settings(), d1)
    view.set_settings(set1, notapath)
    check.equal(view.get_settings(), default)

    d2 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set2}
    view.set_settings(set2, path)
    check.equal(view.get_settings(), d2)
    view.set_settings(set2, notapath)
    check.equal(view.get_settings(), default)

    d3 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set3}
    view.set_settings(set3, path)
    check.equal(view.get_settings(), d3)
    view.set_settings(set3, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set4, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set4, notapath)
    check.equal(view.get_settings(), default)

    d5 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set5}
    view.set_settings(set5, path)
    check.equal(view.get_settings(), d5)
    view.set_settings(set5, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set6, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set6, notapath)
    check.equal(view.get_settings(), default)

    d7 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set7}
    view.set_settings(set7, path)
    check.equal(view.get_settings(), d7)
    view.set_settings(set7, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set8, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set8, notapath)
    check.equal(view.get_settings(), default)

    d9 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set9}
    view.set_settings(set9, path)
    check.equal(view.get_settings(), d9)
    view.set_settings(set9, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set10, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set10, notapath)
    check.equal(view.get_settings(), default)

    d11 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set11}
    view.set_settings(set11, path)
    check.equal(view.get_settings(), d11)
    view.set_settings(set11, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set12, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set12, notapath)
    check.equal(view.get_settings(), default)

    d13 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set13}
    view.set_settings(set13, path)
    check.equal(view.get_settings(), d13)
    view.set_settings(set13, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set14, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set14, notapath)
    check.equal(view.get_settings(), default)

    d15 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set15}
    view.set_settings(set15, path)
    check.equal(view.get_settings(), d15)
    view.set_settings(set15, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set16, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set16, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set17, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set17, notapath)
    check.equal(view.get_settings(), default)

    d18 = {"video": './test/sampleVideo/SampleVideo_1280x720_1mb.mp4', "settings": set18}
    view.set_settings(set18, path)
    check.equal(view.get_settings(), d18)
    view.set_settings(set18, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set19, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set19, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set20, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set20, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set21, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set21, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set22, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set22, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set23, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set23, notapath)
    check.equal(view.get_settings(), default)

    view.set_settings(set24, path)
    check.equal(view.get_settings(), default)
    view.set_settings(set24, notapath)
    check.equal(view.get_settings(), default)


def test_default_settings():
	view = GUI()
	view.set_default_settings()
	check.equal(view.get_settings(), {
        "video": '', "settings": {
            'conf': .5, 'poll': 5, 'anti': 5, 'search': [], 'runtime': 1}})


def test_construct_and_remove():
    view = GUI()
    check.is_true(view.construct_job())
    check.is_true(view.remove_job())
    # combined because kill needs a started Job and this reduces redundancy


def test_render():
    # The theory behind test_render is that the unit tests
    # will test whether render() can put underlying changes
    # of the GUI onto the screen correctly.
    # I will be creating a GUI object, rendering it, leaving it on the screen,
    # then killing it. Then, I will change the underlying paramters
    # then re-render another window.

    # In reality, render() cannot be called or else it messes with the
    # travis build. We will have to figure out a better solution
    # in iteration 2.

    # Another side note is that by the point of rendering the window,
    # all the inputs will be valid. This is because the GUI technically
    # limits the users to edit the settings within a valid range. However,
    # invalid inputs will also be included in testing.
    #
    # The majority of invalid input testing will be in set_settings and get_settings.

    # Good inputs (changes in the paratmeters that are valid) are included
    # to test that the GUI does NOT throw an error message when a valid input
    # is given.

    # If an input is invalid, then the GUI will render the default settings in the GUI.

    # Please note that you cannot touch any of the sliders or values in the GUI between test cases.
    # You must either click "Kill this Window" or click the red X to move to the next test case.

    # First, create a test GUI and make sure the default values are correct when generated.
    test_gui = GUI()
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {'conf': .5, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []})
    check.is_none(test_gui.job)

    # change the video path and settings to some valid input that a user would use
    test_gui.video_path = './test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
    test_gui.set_settings({'conf': .5, 'poll': 3, 'anti': 1, 'runtime': 10, 'search': ['child']}, test_gui.video_path)

    # assert that these changes have gone through
    check.equal(test_gui.video_path, './test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(test_gui.get_settings(), {'settings': {'conf': .5, 'poll': 3, 'anti': 1, 'runtime': 10, 'search': ['child']}, 'video': './test/sampleVideo/SampleVideo_1280x720_1mb.mp4'})
    check.is_none(test_gui.job)

    #test_gui.render()

    # change the video_path, settings, and job to another valid input that a user would use
    test_gui.video_path = './test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
    test_gui.set_settings({'conf': 0.2, 'poll': 1, 'anti': 1, 'runtime': 10, 'search': [
                          "child, kid, ball"]}, test_gui.video_path)
    # create a test job object to use as the test_gui.job parameter
    #test_job1 = Job(test_gui.get_settings())
    #test_gui.job = test_job1
    # assert that these changes have gone through
    check.equal(test_gui.video_path, './test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(test_gui.settings, {'conf': 0.2, 'poll': 1, 'anti': 1, 'runtime': 10, 'search': [
        "child, kid, ball"]})
    #check.equal(test_gui.job, test_job1)

    #test_gui.render()

    # change the video path to a very very long video path.
    test_gui.video_path = './test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
    test_gui.set_settings(test_gui.settings, test_gui.video_path)
    # make sure the other two parameters have not changed, but video path has changed
    check.equal(test_gui.video_path, './test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(test_gui.settings, {'conf': 0.2, 'poll': 1, 'anti': 1, 'runtime': 10, 'search': ["child, kid, ball"]})
    #check.equal(test_gui.job, test_job1)

    #test_gui.render()

    # change the video path to an empty one
    test_gui.video_path = ''
    test_gui.set_settings(test_gui.settings, test_gui.video_path)
    # make sure the correct parameters have changed, and the others have remained the same
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {'conf': 0.2, 'poll': 1, 'anti': 1, 'runtime': 10, 'search': ["child, kid, ball"]})
    #check.equal(test_gui.job, test_job1)

    #test_gui.render()

    # change video path to an invalid value or type
    # the point of this test to make sure that the GUI realizes the invalid input
    # and instead displays the default values.
    # Because these types of errors will be caught by the logic unit tests,
    # most of this testing is done in test_set_settings.

    # Below is an invalid input as the video path is a number, not a string
    test_gui.set_settings({'conf': 0.2, 'poll': 1, 'anti': 1, 'runtime': 10, 'search': ["child, kid, ball"]}, 2)

    # make sure that the parameters have been reset to the default value.
    check.equal(test_gui.video_path, '')
    check.equal(test_gui.settings, {
        'conf': .5, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []})
    #check.equal(test_gui.job, test_job1)

    #test_gui.render()

    # Here, we will start testing more levels of the settings parameter in specific.
    # Valid inputs for settings should not throw a GUI error message and
    # instead display the correct image for the GUI.
    # Incorrect inputs for settings should be reset to the default settings and
    # GUI should display the defaults.

    # create a clean new GUI object
    test_gui2 = GUI()

    # change the video_path to a normal one, make sure GUI displays the new settings
    test_gui2.video_path = './test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
    test_gui2.settings = {'conf': .75, 'poll': 571,
                          'anti': 462, 'runtime': 10, 'search': ["comptuter"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # make sure that these parameters have been appropriately changed
    check.equal(test_gui2.video_path, './test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(test_gui2.settings, {'conf': .75, 'poll': 571,
                          'anti': 462, 'runtime': 10, 'search': ["comptuter"]})
    check.is_none(test_gui2.job)

    #test_gui2.render()

    # change the settings used so there are some invalid values (negative settings)
    test_gui2.settings = {'conf': -10, 'poll': -
                          1, 'anti': -5, 'runtime': 10, 'search': ["uhhhh"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # assert that these changes do not go through and the default settings are implemented
    check.equal(test_gui2.video_path, '')
    check.equal(test_gui2.settings, {'conf': .5, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []})
    check.is_none(test_gui2.job)

    #test_gui2.render()

    # change the settings to the wrong type
    test_gui2.settings = {'conf': 'hello', 'poll': 'nice',
                          'anti': 'should not work', 'runtime': 'woof', 'search': ["seach term"]}
    test_gui2.set_settings(test_gui2.settings, test_gui2.video_path)
    # assert that these changes do not go through and the default settings are rendered
    check.equal(test_gui2.video_path, '')
    check.equal(test_gui2.settings, {'conf': .5, 'poll': 5, 'anti': 5, 'runtime': 1, 'search': []})
    check.is_none(test_gui2.job)

    #test_gui2.render()

    # Here, we will be changing the parameters for the job object.
    # All of the following job objects should be valid and should run.

    # create a new GUI object
    test_gui3 = GUI()

    # change the video_path to something other an empty
    test_gui3.video_path = './test/sampleVideo/SampleVideo_1280x720_1mb.mp4'
    # make the settings something valid for set_settings
    test_gui3.settings = {'conf': .73, 'poll': 93, 'anti': 146, 'runtime': 10, 'search': ['boy']}
    test_gui3.set_settings(test_gui3.settings, test_gui3.video_path)

    # make sure that the job is empty, and the new settings have been achieved.
    check.equal(test_gui3.video_path, './test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(test_gui3.settings, {'conf': .73, 'poll': 93, 'anti': 146, 'runtime': 10, 'search': ['boy']})
    check.is_none(test_gui3.job)

    #test_gui3.render()

    # create a new Job object with the updated settings and path.
    #test_job3 = Job({'settings': test_gui3.settings, 'video': test_gui3.video_path})

    # change the value of the GUI's job
    #test_gui3.job = test_job3
    # make sure job has changed, but all the other settings stay the same
    check.equal(test_gui3.video_path, './test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(test_gui3.settings, {'conf': .73, 'poll': 93, 'anti': 146, 'runtime': 10, 'search': ['boy']})
    #check.equal(test_gui3.job, test_job3)

    #test_gui3.render()

    # change the job back to None
    test_gui3.job = None
    # make sure Job has returned to None, but the other settings remain.
    check.equal(test_gui3.video_path, './test/sampleVideo/SampleVideo_1280x720_1mb.mp4')
    check.equal(test_gui3.settings, {'conf': .73, 'poll': 93, 'anti': 146, 'runtime': 10, 'search': ['boy']})
    check.is_none(test_gui3.job)

    #test_gui3.render()


def test_verify_settings():
    view = GUI()

    check.is_false(view.verify_settings())

    view.set_settings(set1, path)
    check.is_true(view.verify_settings())
    view.set_settings(set1, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set2, path)
    check.is_true(view.verify_settings())
    view.set_settings(set2, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set3, path)
    check.is_true(view.verify_settings())
    view.set_settings(set3, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set4, path)
    check.is_false(view.verify_settings())
    view.set_settings(set4, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set5, path)
    check.is_true(view.verify_settings())
    view.set_settings(set5, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set6, path)
    check.is_false(view.verify_settings())
    view.set_settings(set6, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set7, path)
    check.is_true(view.verify_settings())
    view.set_settings(set7, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set8, path)
    check.is_false(view.verify_settings())
    view.set_settings(set8, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set9, path)
    check.is_false(view.verify_settings())
    view.set_settings(set9, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set10, path)
    check.is_false(view.verify_settings())
    view.set_settings(set10, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set11, path)
    check.is_true(view.verify_settings())
    view.set_settings(set11, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set12, path)
    check.is_false(view.verify_settings())
    view.set_settings(set12, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set13, path)
    check.is_true(view.verify_settings())
    view.set_settings(set13, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set14, path)
    check.is_false(view.verify_settings())
    view.set_settings(set14, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set15, path)
    check.is_true(view.verify_settings())
    view.set_settings(set15, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set16, path)
    check.is_false(view.verify_settings())
    view.set_settings(set16, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set17, path)
    check.is_false(view.verify_settings())
    view.set_settings(set17, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set18, path)
    check.is_true(view.verify_settings())
    view.set_settings(set18, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set19, path)
    check.is_false(view.verify_settings())
    view.set_settings(set19, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set20, path)
    check.is_false(view.verify_settings())
    view.set_settings(set20, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set21, path)
    check.is_false(view.verify_settings())
    view.set_settings(set21, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set22, path)
    check.is_false(view.verify_settings())
    view.set_settings(set22, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set23, path)
    check.is_false(view.verify_settings())
    view.set_settings(set23, notapath)
    check.is_false(view.verify_settings())

    view.set_settings(set24, path)
    check.is_false(view.verify_settings())
    view.set_settings(set24, notapath)
    check.is_false(view.verify_settings())
