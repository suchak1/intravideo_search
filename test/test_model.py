import sys
import pytest
sys.path.append('src')
from model import *  # nopep8


def test_interpret_results():
    job = Job()
    results1 = [(1.0, 0.1), (10.0, 0.03), (20.0, 0.5), (30.0, 1.0)]
    results2 = None
    results3 = []
    results4 =[(-2.0, 0.1)]
    results5 = [(3.0, -0.5)]

    

    with pytest.raises(Exception):
        job.interpret_results(results2)
    with pytest.raises(Exception):
        job.interpret_results(results3)
    with pytest.raises(Exception):
        job.interpret_results(results4)
    with pytest.raises(Exception):
        job.interpret_results(results5)
