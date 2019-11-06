import sys
sys.path.append('src')
from view import *  # nopep8

g = GUI();
assert g.start_job() == 1;

assert g.kill_job() == 1;
