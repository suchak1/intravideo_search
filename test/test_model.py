import sys
import pytest
sys.path.append('src')
from model import *  # nopep8


def test_interpret_results():
    job = Job()

    # -------- Exceptions --------
    # Nonetype
    results1 = None
    with pytest.raises(Exception):
        job.interpret_results(results1)

    # Empty Input
    results2 = []
    with pytest.raises(Exception):
        job.interpret_results(results2)

    # Negative Timestamp
    results3 =[(-2.0, 0.1)]
    with pytest.raises(Exception):
        job.interpret_results(results3)

    # Negative APIScore
    results4 = [(3.0, -0.5)]
    with pytest.raises(Exception):
        job.interpret_results(results4)

    # Duplicate Timestamps
    results5 = [(1.0, 0.1), (1.0, 0.03)]
    with pytest.raises(Exception):
        job.interpret_results(results5)

    # Negative Cutoff Value
    toyResults = [(1.0, 1)]
    with pytest.raises(Exception):
        job.interpret_results(toyResults, cutoff= -0.3)


    # --------- Valid inputs ---------
    # Middle clip
    results6 = [(0.0, 0.1), (10.0, 0.6), (20.0, 0.3), (30.0, 0.2)]
    assert job.interpret_results(results6, cutoff=0.5) == [(5.0, 15.0)]

    # Spanning multiple results
    results7 = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.01)]
    assert job.interpret_results(results7, cutoff=0.5) == [(0.5,25.0)]

    # Multiple clips
    results8 = [(0.0, 0.2), (10.0, 0.6), (20.0, 0.5), (30.0, 0.1),
                                                      (40.0, 0.7),
                                                      (50.0, 0.8),
                                                      (60.0, 0.01)]

    assert job.interpret_results(results8, cutoff=0.5) == \
    [(5.0, 25.0), (35.0, 55.0)]

    # Starting clip
    results9 = [(1.0, 0.6), (10.0, 0.2), (20.0, 0.1), (30.0, 0.08)]
    assert job.interpret_results(results9, cutoff=0.5) == [(0.0, 5.5)]

    # Ending clip
    results10 = [(1.0, 0.2), (10.0, 0.2), (20.0, 0.1), (30.0, 0.8)]
    job.settings = {"endtime", 40.0}
    assert job.interpret_results(results10, cutoff=0.5) == [(25.0, 35.0)]

    # Cutoff of zero
    job.settings = {"endtime", 40.0}
    assert job.interpret_results(results8, cutoff=0.0) ==

    # Cutoff of >1
