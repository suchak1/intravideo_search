from PIL import Image
import sys
import pytest
sys.path.append('src')
from controller import *  # nopep8

def test_constructor():
    w = Worker()
    # Test that the constructor was created correctly and has all the methods
    assert "classify_img" in dir(w)
    assert "make_clip" in dir(w)
    
def test_classify_img():
    img = Image.open(r)
