#!/usr/bin/env python3
"""
test Measure class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.epoch import Event, Span, Epoch
from tests.data.test_data import (df_cycle)

from datetime import datetime



def test_epoch_instance():
    recessions = Epoch(df_cycle)
    assert recessions.df().shape == (13,3)
    results = []
    for idx, col in enumerate(['start', 'end', 'name']):
        result = recessions.df().columns[idx] == col
        results.append(result)
    assert all(results)

def test_epoch_index():
    recessions = Epoch(df_cycle)
    event1 = recessions.idx(2)
    check1 = isinstance(event1, Event)
    dt_str = '2008-01-01'
    event2 = recessions.idx(dt_str)
    check2 = isinstance(event2, Span)
    dt = datetime.strptime(dt_str, '%Y-%m-%d')
    event3 = recessions.idx(dt)
    check3 = isinstance(event3, Span)
    checks = [check1, check2, check3]
    assert all(checks)

#TODO:does to_long have a purpose???
'''
def test_epoch_transformations():
    recessions = Epoch(df_cycle)
    long_recess = recessions.to_long()
    assert long_recess.shape == (0,0)
'''