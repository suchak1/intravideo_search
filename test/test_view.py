import sys
sys.path.append('src')
from view import *  # nopep8

g = GUI();
assert g.start_job() == True;

assert g.kill_job() == False;
