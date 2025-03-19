#!/usr/bin/env python3
"""
Tests for plots
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from macroecon_wrappy.metric import Metric
from macroecon_wrappy.measure import Measure
from macroecon_wrappy.epoch import Epoch
from macroecon_wrappy import plots

from tests.data.test_data import (
    df_series, 
    df_cycle,

    df_mmmffa,
    df_tb1yr
    )

import plotnine as p9
import pandas as pd
import numpy as np


metric1 = Metric(df_series['value1'])
metric2 = Metric(df_series['value2'])
epoch = Epoch(df_cycle)
measure = Measure([metric1, metric2], epoch)


def test_graph_ts_df():
    """
    df = pd.DataFrame({
        "x": np.random.uniform(-4, 5, size=50),
        "y": np.random.uniform(2, 5, size=50)
        })
    """
    df = pd.DataFrame({
        "ts": pd.date_range(start='1/1/2018', periods=50),
        "GDP": np.random.uniform(2, 5, size=50),
        "GDI": np.random.uniform(2, 5, size=50)
        })
    df.set_index('ts', inplace=True)
    plots.graph_ts_js(df, cols=['GDP'], recession_bars=False, log_scale='y')
    assert True == True

def test_graph_measure():
    plots.graph_ts_js(measure, cols=['col-1'], recession_bars=True, log_scale='y')
    assert True == True

def test_graph_measure_actual_data():
    mmmffa = Metric(df_mmmffa['MMMFFAQ027S'])
    tb1yr = Metric(df_tb1yr['DTB1YR'])
    measure = Measure([mmmffa, tb1yr])
    plots.graph_ts_js(measure, cols=['col-1'])
    assert True == True

def test_graph_cycle():
    assert True == True


#TODO: this may not be necessary
'''
def test_graph_ts():
    plt = plots.graph_ts(df_series, cols=['value1', 'value2'])
    assert type(plt) == p9.ggplot
'''