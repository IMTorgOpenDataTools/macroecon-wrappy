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
import numpy as np








def test_metric_basic():
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

def test_metric_advanced():
    date_range = pd.date_range(start='2023-01-01', periods=72, freq='H')   #define a date range (e.g., hourly data for 72 periods)
    np.random.seed(42)
    random_values = np.abs(np.round(np.random.randn(len(date_range)), decimals=2))    #generate random data for the values (e.g., using numpy.random.randn)
    ts = pd.Series(random_values, index=date_range)
    metric1 = Metric(ts)
    metric1.set_metadata(title='title1')
    #time change
    daily_metric = metric1.change_time(rule='D')
    daily_metric_rounded = np.round(daily_metric.tolist(), decimals=2)
    assert daily_metric_rounded.tolist() == [0.78, 0.72, 0.74]
    #returns
    cumulative_returns = metric1.returns(type='cumulative')
    cumulative_returns_head = np.round(cumulative_returns, decimals=2).tolist()[-4:]
    assert cumulative_returns_head == [0.72, 1.3, 0.72, 3.08]
    #exponential moving average
    ema = metric1.ema(span=20)
    ema_head = np.round(ema.tolist()[:4],decimals=2).tolist()
    assert ema_head == [0.5, 0.47, 0.48, 0.58]
    #moments
    historical_volitility = metric1.returns(type='log').moment_values(type='VOL', trading_days=70)
    historical_volitility_head = np.round(historical_volitility, decimals=2).tolist()[-4:]
    assert historical_volitility_head == [10.5, 10.35, 9.93, 9.79]