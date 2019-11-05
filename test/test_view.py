import sys
sys.path.append('src')
from view import *  # nopep8


def test_set_settings():
	set1 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet']} #should be true
	set2 = {'conf': 0.1, 'poll': 2, 'anti': 8, 'search' = ['car']} #should be true
	set3 = {'conf': 0, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet']} #should be true
	set4 = {'conf': -0.1, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet']} #should be false, conf is negative
	set5 = {'conf': 1.0, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet']} #should be true
	set6 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet']} #should be false, conf is >1
	set7 = {'conf': 0.9, 'poll': 0, 'anti': 5, 'search' = ['dog', 'pet']} #should be true
	set8 = {'conf': 1.1, 'poll': -1, 'anti': 5, 'search' = ['dog', 'pet']} #should be false, poll is < 0
	set9 = {'conf': 1.1, 'poll': 500000, 'anti': 5, 'search' = ['dog', 'pet']} #should be true
	set10 = {'conf': 1.1, 'poll': 5.2, 'anti': 5, 'search' = ['dog', 'pet']} #should be false, poll is not an integer
	set11 = {'conf': 1.1, 'poll': 5, 'anti': 0, 'search' = ['dog', 'pet']} #should be true
	set12 = {'conf': 1.1, 'poll': 5, 'anti': -1, 'search' = ['dog', 'pet']} #should be false, anti is < 0
	set13 = {'conf': 1.1, 'poll': 5, 'anti': 5000000, 'search' = ['dog', 'pet']} #should be true
	set14 = {'conf': 1.1, 'poll': 5, 'anti': 5.2, 'search' = ['dog', 'pet']} #should be false, anti is not an integer
	set15 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet', '50']} #should be true
	set16 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search' = []} #should be false, no search terms
	set17 = {'conf': 1.1, 'poll': 5, 'anti': 5, 'search' = [84, '84']} #should be false, one value is not a string

	set18 = {'search' = ['dog', 'pet'], 'poll': 5, 'conf': 1.1, 'anti': 5} #should be true, even if out of order
	set19 = {'poll': 5, 'anti': 5, 'search' = ['dog', 'pet']} #should be false
	set20 = {'conf': 1.1, 'anti': 5, 'search' = ['dog', 'pet']} #should be false
	set21 = {'conf': 1.1, 'poll': 5, 'search' = ['dog', 'pet']} #should be false
	set22 = {'conf': 1.1, 'poll': 5, 'anti': 5} #should be false
	set23 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet'], 'video' = 'path/to/video'} #should be false, extra key
	set24 = {'conf': 0.9, 'poll': 5, 'anti': 5, 'search' = ['dog', 'pet'], 'x' = 0} #should be false

	path = 'here/is/a/path'
	notapath = 52

	#assertion statements, there will be 48 cases
	assert set_settings(set1, path) == True
	assert set_settings(set1, notapath) == False
	assert set_settings(set2, path) == True
	assert set_settings(set2, notapath) == False
	assert set_settings(set3, path) == True
	assert set_settings(set3, notapath) == False
	assert set_settings(set4, path) == False
	assert set_settings(set4, notapath) == False
	assert set_settings(set5, path) == True
	assert set_settings(set5, notapath) == False
	assert set_settings(set6, path) == False
	assert set_settings(set6, notapath) == False
	assert set_settings(set7, path) == True
	assert set_settings(set7, notapath) == False
	assert set_settings(set8, path) == True
	assert set_settings(set8, notapath) == False
	assert set_settings(set9, path) == False
	assert set_settings(set9, notapath) == False
	assert set_settings(set10, path) == True
	assert set_settings(set10, notapath) == False
	assert set_settings(set11, path) == False
	assert set_settings(set11, notapath) == False
	assert set_settings(set12, path) == True
	assert set_settings(set12, notapath) == False
	assert set_settings(set13, path) == True
	assert set_settings(set13, notapath) == False
	assert set_settings(set14, path) == False
	assert set_settings(set14, notapath) == False
	assert set_settings(set15, path) == True
	assert set_settings(set15, notapath) == False
	assert set_settings(set16, path) == False
	assert set_settings(set16, notapath) == False
	assert set_settings(set17, path) == False
	assert set_settings(set17, notapath) == False
	assert set_settings(set18, path) == True
	assert set_settings(set18, notapath) == False
	assert set_settings(set19, path) == False
	assert set_settings(set19, notapath) == False
	assert set_settings(set20, path) == False
	assert set_settings(set20, notapath) == False
	assert set_settings(set21, path) == False
	assert set_settings(set21, notapath) == False
	assert set_settings(set22, path) == False
	assert set_settings(set22, notapath) == False
	assert set_settings(set23, path) == False
	assert set_settings(set23, notapath) == False
	assert set_settings(set24, path) == False
	assert set_settings(set24, notapath) == False


def test_get_settings():
	pass