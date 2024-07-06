#!/usr/bin/env python3
"""
test Measure class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.metric import Metric
from macroecon_wrappy.measure import Measure
from tests.data.test_data import df_series

import pandas as pd



def test_measure():
    metric1 = Metric(df_series['value1'])
    metric2 = Metric(df_series['value2'])
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
    long = measure.to_long()
    assert long.shape == (12,3)