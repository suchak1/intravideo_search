import sys
sys.path.append('../src')
from view import *  # nopep8


def test_render():
    return 0

def test_constructor():

    # Currently, when the GUI object is created, we are only allowing
    # the default values to be used.

    # test default constructor with no paramters
    test_gui = GUI()
    assert test_gui.video_path == ''
    assert test_gui.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': [""]}
    assert test_gui.job == None

    return 0

test_constructor()
test_render()
