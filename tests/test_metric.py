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
    assert metric1.values.__len__() == df_series.shape[0]