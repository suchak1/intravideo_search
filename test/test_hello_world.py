import sys
sys.path.append('src')
from hello_world import * # nopep8



def test_main():
    assert main() == None

test_main()
