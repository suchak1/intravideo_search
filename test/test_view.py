import sys
sys.path.append('../src')
from view import *  # nopep8


def test_render():
    return 0

def test_constructor():
    test_gui = GUI()
    assert test_gui.video_path == ''
    assert test_gui.settings == {'conf': .9, 'poll': 5, 'anti': 5, 'search': ["dog"]}
    assert test_gui.job == None
    return 0

test_constructor()
test_render()
