# -*- coding: utf-8 -*-
import sys
sys.path.append('src') #note: this only works if you're in the parent directory, not the test directory
from view import *  # nopep8


def test_set_settings():
	view = GUI()
	set1 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	set2 = {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']} #should be true
	set3 = {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is negative
	set5 = {'conf': 1.0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is >1
	set7 = {'conf': 0.9, 'poll': 0, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	set8 = {'conf': 1.1, 'poll': -1, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is < 0
	set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is not an integer
	set11 = {'conf': 1.1, 'poll': 5, 'anti': 0, 'search': ['dog', 'pet']} #should be true
	set12 = {'conf': 1.1, 'poll': 5, 'anti': -1, 'search': ['dog', 'pet']} #should be false, anti is < 0
	set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000, 'search': ['dog', 'pet']} #should be true
	set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': ['dog', 'pet']} #should be false, anti is not an integer
	set15 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet', '50']} #should be true
	set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []} #should be false, no search terms
	set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']} #should be false, one value is not a string

	set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5} #should be true, even if out of order
	set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	set20 = {'conf': 1.1, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	set21 = {'conf': 1.1, 'poll': 5, 'search': ['dog', 'pet']} #should be false
	set22 = {'conf': 1.1, 'poll': 5, 'anti': 5} #should be false
	set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'video': 'path/to/video'} #should be false, extra key
	set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'x': 0} #should be false

	path = 'here/is/a/path'
	notapath = 52

	#assertion statements, there will be 48 cases
	assert view.set_settings(set1, path) == True
	assert view.set_settings(set1, notapath) == False
	assert view.set_settings(set2, path) == True
	assert view.set_settings(set2, notapath) == False
	assert view.set_settings(set3, path) == True
	assert view.set_settings(set3, notapath) == False
	assert view.set_settings(set4, path) == False
	assert view.set_settings(set4, notapath) == False
	assert view.set_settings(set5, path) == True
	assert view.set_settings(set5, notapath) == False
	assert view.set_settings(set6, path) == False
	assert view.set_settings(set6, notapath) == False
	assert view.set_settings(set7, path) == True
	assert view.set_settings(set7, notapath) == False
	assert view.set_settings(set8, path) == True
	assert view.set_settings(set8, notapath) == False
	assert view.set_settings(set9, path) == False
	assert view.set_settings(set9, notapath) == False
	assert view.set_settings(set10, path) == True
	assert view.set_settings(set10, notapath) == False
	assert view.set_settings(set11, path) == False
	assert view.set_settings(set11, notapath) == False
	assert view.set_settings(set12, path) == True
	assert view.set_settings(set12, notapath) == False
	assert view.set_settings(set13, path) == True
	assert view.set_settings(set13, notapath) == False
	assert view.set_settings(set14, path) == False
	assert view.set_settings(set14, notapath) == False
	assert view.set_settings(set15, path) == True
	assert view.set_settings(set15, notapath) == False
	assert view.set_settings(set16, path) == False
	assert view.set_settings(set16, notapath) == False
	assert view.set_settings(set17, path) == False
	assert view.set_settings(set17, notapath) == False
	assert view.set_settings(set18, path) == True
	assert view.set_settings(set18, notapath) == False
	assert view.set_settings(set19, path) == False
	assert view.set_settings(set19, notapath) == False
	assert view.set_settings(set20, path) == False
	assert view.set_settings(set20, notapath) == False
	assert view.set_settings(set21, path) == False
	assert view.set_settings(set21, notapath) == False
	assert view.set_settings(set22, path) == False
	assert view.set_settings(set22, notapath) == False
	assert view.set_settings(set23, path) == False
	assert view.set_settings(set23, notapath) == False
	assert view.set_settings(set24, path) == False
	assert view.set_settings(set24, notapath) == False


def test_get_settings():
	"""
		Assumption: If set_settings fails, the default values are set for all of the parameters
	"""

	view = GUI()
	default = {"video": '', "settings": {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': []}}

	set1 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d1 = {"video": 'here/is/a/path', "settings": {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}

	set2 = {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']} #should be true
	d2 = {"video": 'here/is/a/path', "settings": {'conf': 0.1, 'poll': 2, 'anti': 8, 'search': ['car']}} 
	set3 = {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d3 = {"video": 'here/is/a/path', "settings": {'conf': 0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']}}
	set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is negative
	set5 = {'conf': 1.0, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d5 = {"video": 'here/is/a/path', "settings": set5}
	set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false, conf is >1
	set7 = {'conf': 0.9, 'poll': 0, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d7 = {"video": 'here/is/a/path', "settings": set7}
	set8 = {'conf': 1.1, 'poll': -1, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is < 0
	set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5, 'search': ['dog', 'pet']} #should be true
	d9 = {"video": 'here/is/a/path', "settings": set9}
	set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search': ['dog', 'pet']} #should be false, poll is not an integer
	set11 = {'conf': 1.1, 'poll': 5, 'anti': 0, 'search': ['dog', 'pet']} #should be true
	d11 = {"video": 'here/is/a/path', "settings": set11}
	set12 = {'conf': 1.1, 'poll': 5, 'anti': -1, 'search': ['dog', 'pet']} #should be false, anti is < 0
	set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000, 'search': ['dog', 'pet']} #should be true
	d13 = {"video": 'here/is/a/path', "settings": set13}
	set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search': ['dog', 'pet']} #should be false, anti is not an integer
	set15 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet', '50']} #should be true
	set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': []} #should be false, no search terms
	set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search': [84, '84']} #should be false, one value is not a string

	set18 = {'search': ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5} #should be true, even if out of order
	set19 = {'poll': 5, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	set20 = {'conf': 1.1, 'anti': 5, 'search': ['dog', 'pet']} #should be false
	set21 = {'conf': 1.1, 'poll': 5, 'search': ['dog', 'pet']} #should be false
	set22 = {'conf': 1.1, 'poll': 5, 'anti': 5} #should be false
	set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'video': 'path/to/video'} #should be false, extra key
	set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search': ['dog', 'pet'], 'x': 0} #should be false
	path = 'here/is/a/path'
	notapath = 52
	#we need to set and get
	

	assert view.get_settings() == default #should be the default

	view.set_settings(set1, path)
	assert view.get_settings() == d1
	view.set_settings(set1, notapath)
	assert view.get_settings() == default
	view.set_settings(set2, path)
	assert view.get_settings == d2
	view.set_settings(set2, notapath)
	assert view.get_settings() == default
	view.set_settings(set3, path)
	assert view.get_settings() == d3
	view.set_settings(set3, notapath)
	assert view.get_settings() == default
	view.set_settings(set4, path)
	assert view.get_settings() == default
	view.set_settings(set4, notapath)
	assert view.get_settings() == default
	view.set_settings(set5, path)
	assert view.get_settings() == d5
	view.set_settings(set5, notapath)
	assert view.get_settings() == default
	view.set_settings(set6, path)
	assert view.get_settings() == default
	view.set_settings(set6, notapath)
	assert view.get_settings() == default
	view.set_settings(set7, path)
	assert view.get_settings() == d7
	view.set_settings(set7, notapath)
	assert view.get_settings() == default
	view.set_settings(set8, path)
	assert view.get_settings() == d8
	view.set_settings(set8, notapath)
	assert view.get_settings() == default
	view.set_settings(set9, path)
	assert view.get_settings() == default
	view.set_settings(set9, notapath)
	assert view.get_settings() == default
	view.set_settings(set10, path)
	assert view.get_settings() == d10
	view.set_settings(set10, notapath)
	assert view.get_settings() == default
	view.set_settings(set11, path)
	assert view.get_settings() == default
	view.set_settings(set11, notapath)
	assert view.get_settings() == default
	view.set_settings(set12, path)
	assert view.get_settings() == d12
	view.set_settings(set12, notapath)
	assert view.get_settings() == default
	view.set_settings(set13, path)
	assert view.get_settings() == d13
	view.set_settings(set13, notapath)
	assert view.get_settings() == default
	view.set_settings(set14, path)
	assert view.get_settings() == default
	view.set_settings(set14, notapath)
	assert view.get_settings() == default
	view.set_settings(set15, path)
	assert view.get_settings() == d15
	view.set_settings(set15, notapath)
	assert view.get_settings() == default
	view.set_settings(set16, path)
	assert view.get_settings() == default
	view.set_settings(set16, notapath)
	assert view.get_settings() == default
	view.set_settings(set17, path)
	assert view.get_settings() == default
	view.set_settings(set17, notapath)
	assert view.get_settings() == default
	view.set_settings(set18, path)
	assert view.get_settings() == d18
	view.set_settings(set18, notapath)
	assert view.get_settings() == default
	view.set_settings(set19, path)
	assert view.get_settings() == default
	view.set_settings(set19, notapath)
	assert view.get_settings() == default
	view.set_settings(set20, path)
	assert view.get_settings() == default
	view.set_settings(set20, notapath)
	assert view.get_settings() == default
	view.set_settings(set21, path)
	assert view.get_settings() == default
	view.set_settings(set21, notapath)
	assert view.get_settings() == default
	view.set_settings(set22, path)
	assert view.get_settings() == default
	view.set_settings(set22, notapath)
	assert view.get_settings() == default
	view.set_settings(set23, path) 
	assert view.get_settings() == default
	view.set_settings(set23, notapath)
	assert view.get_settings() == default
	view.set_settings(set24, path)
	assert view.get_settings() == default
	view.set_settings(set24, notapath)
	assert view.get_settings() == default


