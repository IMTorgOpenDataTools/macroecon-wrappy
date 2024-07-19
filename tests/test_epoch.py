#!/usr/bin/env python3
"""
test Measure class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.epoch import Event, Epoch
from tests.data.test_data import (df_cycle)

from datetime import datetime



def test_epoch_instance():
    recessions = Epoch(df_cycle)
    assert recessions.df().shape == (11,2)
    results = []
    for idx, col in enumerate(['start', 'end']):
        result = recessions.df().columns[idx] == col
        results.append(result)
    assert all(results)

def test_epoch_index():
    recessions = Epoch(df_cycle)
    event1 = recessions.idx(9)
    dt_str = '2008-01-01'
    event2 = recessions.idx(dt_str)
    dt = datetime.strptime(dt_str, '%Y-%m-%d')
    event3 = recessions.idx(dt)
    check = [isinstance(item, Event) for item in [event1, event2, event3]]
    assert all(check)

def test_epoch_transformations():
    recessions = Epoch(df_cycle)
    long_recess = recessions.to_long()
    assert long_recess.shape == (0,0)