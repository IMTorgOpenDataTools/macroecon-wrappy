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
cycle = Epoch(df_cycle)


def test_measure_instance():
    measure = Measure([metric1, metric2])
    df = measure.df()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (6,2)
    results = []
    for idx, name in enumerate(['col-0', 'col-1']):
        result = df.columns[idx]==name
        results.append(result)
    assert all(results)
    assert isinstance(df.index, pd.core.indexes.datetimes.DatetimeIndex)
    measure = Measure([metric1, metric2], cycle)
    assert measure.df(cycle=True).shape == (35,2)


def test_measure_transformations():
    measure = Measure([metric1, metric2], cycle)
    long = measure.to_long()
    assert long.shape == (12,3)
    #long_cycle = measure.to_long_by_cycle()