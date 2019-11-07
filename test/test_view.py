# -*- coding: utf-8 -*-
import sys
sys.path.append('src') #note: this only works if you're in the parent directory, not the test directory
from view import *  # nopep8


def test_set_settings():
	path = 'here/is/a/path'
	notapath = 52


	view = GUI()
	set1 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set1, path) == True
	assert view.set_settings(set1, notapath) == False

	set2 = {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']} #should be true
	assert view.set_settings(set2, path) == True
	assert view.set_settings(set2, notapath) == False

	set3 = {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set3, path) == True
	assert view.set_settings(set3, notapath) == False

	set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is negative
	assert view.set_settings(set4, path) == False
	assert view.set_settings(set4, notapath) == False

	set5 = {'conf': 1.0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set5, path) == True
	assert view.set_settings(set5, notapath) == False

	set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is >1
	assert view.set_settings(set6, path) == False
	assert view.set_settings(set6, notapath) == False

	set7 = {'conf': 0.9, 'poll': 0, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set7, path) == True
	assert view.set_settings(set7, notapath) == False

	set8 = {'conf': 1.1, 'poll': -1, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is < 0
	assert view.set_settings(set8, path) == True
	assert view.set_settings(set8, notapath) == False

	set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set9, path) == False
	assert view.set_settings(set9, notapath) == False

	set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is not an integer
	assert view.set_settings(set10, path) == True
	assert view.set_settings(set10, notapath) == False

	set11 = {'conf': 1.1, 'poll': 5, 'anti': 0, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set11, path) == False
	assert view.set_settings(set11, notapath) == False

	set12 = {'conf': 1.1, 'poll': 5, 'anti': -1, 'search': ['dog', 'pet']} #should be false, anti is < 0
	assert view.set_settings(set12, path) == True
	assert view.set_settings(set12, notapath) == False

	set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000, 'search': ['dog', 'pet']} #should be true
	assert view.set_settings(set13, path) == True
	assert view.set_settings(set13, notapath) == False

	set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': ['dog', 'pet']} #should be false, anti is not an integer
	assert view.set_settings(set14, path) == False
	assert view.set_settings(set14, notapath) == False

	set15 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet', '50']} #should be true
	assert view.set_settings(set15, path) == True
	assert view.set_settings(set15, notapath) == False

	set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []} #should be false, no search terms
	assert view.set_settings(set16, path) == False
	assert view.set_settings(set16, notapath) == False

	set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']} #should be false, one value is not a string
	assert view.set_settings(set17, path) == False
	assert view.set_settings(set17, notapath) == False

	set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5} #should be true, even if out of order
	assert view.set_settings(set18, path) == True
	assert view.set_settings(set18, notapath) == False

	set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	assert view.set_settings(set19, path) == False
	assert view.set_settings(set19, notapath) == False

	set20 = {'conf': 1.1, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	assert view.set_settings(set20, path) == False
	assert view.set_settings(set20, notapath) == False

	set21 = {'conf': 1.1, 'poll': 5, 'search': ['dog', 'pet']} #should be false
	assert view.set_settings(set21, path) == False
	assert view.set_settings(set21, notapath) == False

	set22 = {'conf': 1.1, 'poll': 5, 'anti': 5} #should be false
	assert view.set_settings(set22, path) == False
	assert view.set_settings(set22, notapath) == False

	set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'video': 'path/to/video'} #should be false, extra key
	assert view.set_settings(set23, path) == False
	assert view.set_settings(set23, notapath) == False

	set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'x': 0} #should be false
	assert view.set_settings(set24, path) == False
	assert view.set_settings(set24, notapath) == False
	


def test_get_settings():
	"""
		Assumption: If set_settings fails, the default values are set for all of the parameters
	"""

	path = 'here/is/a/path'
	notapath = 52

	view = GUI()
	default = {"video": '', "settings": {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': []}} #default settings
	assert view.get_settings() == default #should be the default

	set1 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d1 = {"video": 'here/is/a/path', "settings": {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}
	view.set_settings(set1, path)
	assert view.get_settings() == d1
	view.set_settings(set1, notapath)
	assert view.get_settings() == default

	set2 = {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']} #should be true
	d2 = {"video": 'here/is/a/path', "settings": {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']}} 
	view.set_settings(set2, path)
	assert view.get_settings == d2
	view.set_settings(set2, notapath)
	assert view.get_settings() == default

	set3 = {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d3 = {"video": 'here/is/a/path', "settings": {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}
	view.set_settings(set3, path)
	assert view.get_settings() == d3
	view.set_settings(set3, notapath)
	assert view.get_settings() == default

	set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is negative
	view.set_settings(set4, path)
	assert view.get_settings() == default
	view.set_settings(set4, notapath)
	assert view.get_settings() == default

	set5 = {'conf': 1.0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d5 = {"video": 'here/is/a/path', "settings": set5}
	view.set_settings(set5, path)
	assert view.get_settings() == d5
	view.set_settings(set5, notapath)
	assert view.get_settings() == default


	set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is >1
	view.set_settings(set6, path)
	assert view.get_settings() == default
	view.set_settings(set6, notapath)
	assert view.get_settings() == default

	set7 = {'conf': 0.9, 'poll': 0, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d7 = {"video": 'here/is/a/path', "settings": set7}
	view.set_settings(set7, path)
	assert view.get_settings() == d7
	view.set_settings(set7, notapath)
	assert view.get_settings() == default

	set8 = {'conf': 1.1, 'poll': -1, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is < 0
	view.set_settings(set8, path)
	assert view.get_settings() == default
	view.set_settings(set8, notapath)
	assert view.get_settings() == default

	set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d9 = {"video": 'here/is/a/path', "settings": set9}
	view.set_settings(set9, path)
	assert view.get_settings() == d9
	view.set_settings(set9, notapath)
	assert view.get_settings() == default

	set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is not an integer
	view.set_settings(set10, path)
	assert view.get_settings() == default
	view.set_settings(set10, notapath)
	assert view.get_settings() == default

	set11 = {'conf': 1.1, 'poll': 5, 'anti': 0, 'search': ['dog', 'pet']} #should be true
	d11 = {"video": 'here/is/a/path', "settings": set11}
	view.set_settings(set11, path)
	assert view.get_settings() == d11
	view.set_settings(set11, notapath)
	assert view.get_settings() == default

	set12 = {'conf': 1.1, 'poll': 5, 'anti': -1, 'search': ['dog', 'pet']} #should be false, anti is < 0
	view.set_settings(set12, path)
	assert view.get_settings() == defaults
	view.set_settings(set12, notapath)
	assert view.get_settings() == default

	set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000, 'search': ['dog', 'pet']} #should be true
	d13 = {"video": 'here/is/a/path', "settings": set13}
	view.set_settings(set13, path)
	assert view.get_settings() == d13
	view.set_settings(set13, notapath)
	assert view.get_settings() == default

	set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': ['dog', 'pet']} #should be false, anti is not an integer
	view.set_settings(set14, path)
	assert view.get_settings() == default
	view.set_settings(set14, notapath)
	assert view.get_settings() == default

	set15 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet', '50']} #should be true
	d15 = {"video": 'here/is/a/path', "settings": set15}
	view.set_settings(set15, path)
	assert view.get_settings() == d15
	view.set_settings(set15, notapath)
	assert view.get_settings() == default

	set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []} #should be false, no search terms
	view.set_settings(set16, path)
	assert view.get_settings() == default
	view.set_settings(set16, notapath)
	assert view.get_settings() == default

	set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']} #should be false, one value is not a string
	view.set_settings(set17, path)
	assert view.get_settings() == default
	view.set_settings(set17, notapath)
	assert view.get_settings() == default

	set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5} #should be true, even if out of order
	d18 = {"video": 'here/is/a/path', "settings": set18}
	view.set_settings(set18, path)
	assert view.get_settings() == d18
	view.set_settings(set18, notapath)
	assert view.get_settings() == default

	set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	view.set_settings(set19, path)
	assert view.get_settings() == default
	view.set_settings(set19, notapath)
	assert view.get_settings() == default

	set20 = {'conf': 1.1, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	view.set_settings(set20, path)
	assert view.get_settings() == default
	view.set_settings(set20, notapath)
	assert view.get_settings() == default

	set21 = {'conf': 1.1, 'poll': 5, 'search': ['dog', 'pet']} #should be false
	view.set_settings(set21, path)
	assert view.get_settings() == default
	view.set_settings(set21, notapath)
	assert view.get_settings() == default

	set22 = {'conf': 1.1, 'poll': 5, 'anti': 5} #should be false
	view.set_settings(set22, path)
	assert view.get_settings() == default
	view.set_settings(set22, notapath)
	assert view.get_settings() == default

	set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'video': 'path/to/video'} #should be false, extra key
	view.set_settings(set23, path) 
	assert view.get_settings() == default
	view.set_settings(set23, notapath)
	assert view.get_settings() == default

	set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'x': 0} #should be false
	view.set_settings(set24, path)
	assert view.get_settings() == default
	view.set_settings(set24, notapath)
	assert view.get_settings() == default


