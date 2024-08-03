#!/usr/bin/env python3
"""
test Measure class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.metric import Metric
from macroecon_wrappy.measure import Measure
from macroecon_wrappy.epoch import Epoch
from tests.data.test_data import (df_series, df_cycle)

import pandas as pd


metric1 = Metric(df_series['value1'])
metric2 = Metric(df_series['value2'])
epoch = Epoch(df_cycle)


def test_measure_instance():
    measure = Measure([metric1, metric2])
    assert isinstance(measure.df(), pd.DataFrame)
    assert measure.df().shape == (6,2)
    results = []
    for idx, name in enumerate(['col-0', 'col-1']):
        result = measure.df().columns[idx]==name
        results.append(result)
    assert all(results)
    assert isinstance(measure.df().index, pd.core.indexes.datetimes.DatetimeIndex)
    measure = Measure([metric1, metric2], epoch)
    assert measure.df().shape == (6,2)
    assert measure.get_cycle().df().shape == (13,3)


def test_measure_transformations():
    measure = Measure([metric1, metric2], epoch)
    measure.to_long()
    assert measure.to_long().shape == (12,2)
    assert measure.to_long().index.name == 'timestamp'
    #long_cycle = measure.to_long_by_cycle()