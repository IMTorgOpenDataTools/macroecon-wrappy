#!/usr/bin/env python3
"""
test Measure class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.metric import Metric
from tests.data.test_data import df_series

import pandas as pd



def test_metric():
    ts = df_series['value1']
    metric1 = Metric(ts)
    metric1.set_metadata(title='title1')
    #series index
    assert type(metric1.index) == pd.DatetimeIndex
    assert type(metric1.index[0]) == pd.Timestamp
    #series attributes
    assert metric1.values.__len__() == df_series.shape[0]
    assert metric1.shape == (16,)
    #series methods
    assert metric1.T.size == 16
    assert metric1.T.shape == (16,)
    #metric attributes
    assert metric1.title == 'title1'
    assert metric1.get_metadata()['title'] == 'title1'