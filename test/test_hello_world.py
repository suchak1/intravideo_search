import pytest
import pipreqs
import sys
sys.path.append('src')
from hello_world import *

def test_main():
    assert main() == None
