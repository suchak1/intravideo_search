import sys
sys.path.append('src')
from view import *  # nopep8
#from model import *
import tkinter as tk

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


def test_constructor():

    # Currently, when the GUI object is created, we are only allowing
    # the default values to be used.

    # test default constructor with no paramters
    test_gui = GUI()
    assert test_gui.video_path == ''
    assert test_gui.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""]}
    assert test_gui.job == None

    return 0

# test_constructor()
# test_render()
