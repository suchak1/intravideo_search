import sys
import pytest
sys.path.append('src')
from model import *  # nopep8


def test_interpret_results_null_input():
    job = Job()
    results = None
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_empty_input():
    job = Job()
    results = []
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_negative_time():
    job = Job()
    results =[(-2.0, 0.1)]
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_negative_score():
    job = Job()
    results = [(3.0, -0.5)]
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_unnormalized_score():
    job = Job()
    resultsNonNorm = [(3.0, 1.2)]
    with pytest.raises(Exception):
        job.interpret_results(resultsNonNorm)

def test_interpret_results_duplicate_times():
    job = Job()
    results = [(1.0, 0.1), (1.0, 0.03)]
    with pytest.raises(Exception):
        job.interpret_results(results)

def test_interpret_results_negative_cutoff():
    job = Job()
    toyResults = [(1.0, 1)]
    with pytest.raises(Exception):
        job.interpret_results(toyResults, cutoff= -0.3)

def test_interpret_results_out_of_order():
    job = Job()
    results1 = [(3.0, 0.6), (1.0, 0.03)]
    results2 = [(1.0, 0.03), (3.0, 0.6)]
    times1 = job.interpret_results(results1)
    times2 = job.interpret_results(results2)
    assert stampListsAreEqual(times1, times2)


def test_interpret_results_mid_clip():
    job = Job()
    results = [(0.0, 0.1), (10.0, 0.6), (20.0, 0.3), (30.0, 0.2)]
    assert job.interpret_results(results, cutoff=0.5) == [(5.0, 15.0)]

def test_interpret_results_spanning_clip():
    job = Job()
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.01)]
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5), [(0.5,25.0)])

def test_interpret_results_multiple_seperate_clips():
    job = Job()
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.1),
                                                      (40.0, 0.7),
                                                      (50.0, 0.8),
                                                      (60.0, 0.01)]

    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                                [(5.0, 25.0), (35.0, 55.0)])

def test_interpret_results_from_start():
    job = Job()
    results = [(1.0, 0.6), (10.0, 0.2), (20.0, 0.1), (30.0, 0.08)]
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                                            [(0.0, 5.5)])

def test_interpret_results_from_end():
    job = Job()
    results = [(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
    job.settings = {"endtime", 40.0}
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.5),
                                                            [(25.0, 40.0)])

def test_interpret_results_zero_cutoff():
    job = Job()
    results = [(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
    job.settings = {"endtime", 40.0}
    assert stampListsAreEqual(job.interpret_results(results, cutoff=0.0),
                                                                [(0.0, 40.0)])

def test_interpret_results_cutoff_morethan_1():
    job = Job()
    results = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.1),
                                                      (40.0, 0.7),
                                                      (50.0, 0.8),
                                                      (60.0, 0.01)]
    assert stampListsAreEqual(job.interpret_results(results, cutoff=1.1), [])

def stampListsAreEqual(times1, times2):
    if not isinstance(times1, type([])) or \
       not isinstance(times2, type([])) or \
       not (len(times1) == len(times2)):
       return False

    for i in range(len(times1)):
        if not (times1[i] == times2[i]):
            return False

    return True
