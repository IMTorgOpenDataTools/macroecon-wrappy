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
from tests.data.test_data import (
    df_series, 
    df_cycle,

    df_mmmffa,
    df_tb1yr
    )

import pandas as pd
import numpy as np


metric1 = Metric(df_series['value1'])
metric2 = Metric(df_series['value2'])
epoch = Epoch(df_cycle)


def test_measure_instance():
    #data without cycle
    measure = Measure([metric1, metric2])
    assert repr(measure) == '\n        Metrics: \n            None(col-0)  None(col-1)\ntimestamp                           \n1990-01-01       1000.0        950.0\n1988-01-01        800.0        900.0\n1987-01-01        900.0        500.0\n1986-01-01        800.0        300.0\n1984-01-01          NaN        800.0\n        Cycle: \nno self.cycle of `Epoch` is available.  use measure.set_cycle(cycle) \n        '
    assert isinstance(measure.df(), pd.DataFrame)
    assert measure.df().shape == (16,2)
    #column names
    results = []
    for idx, name in enumerate(['col-0', 'col-1']):
        result = measure.df().columns[idx]==name
        results.append(result)
    assert all(results)
    #index
    assert isinstance(measure.df().index, pd.core.indexes.datetimes.DatetimeIndex)
    #data with cycle
    measure = Measure([metric1, metric2], epoch)
    assert repr(measure) == '\n        Metrics: \n            None(col-0)  None(col-1)\ntimestamp                           \n1990-01-01       1000.0        950.0\n1988-01-01        800.0        900.0\n1987-01-01        900.0        500.0\n1986-01-01        800.0        300.0\n1984-01-01          NaN        800.0\n        Cycle: \n       start        end name\n0 1953-07-01 1954-05-01     \n1 1957-08-01 1958-04-01     \n2 1960-01-01 1960-01-01     \n3 1960-04-01 1961-02-01     \n4 1969-12-01 1970-11-01      \n        '
    assert measure.df().shape == (16,2)
    assert measure.get_cycle().df().shape == (13,3)

def test_measure_get_cycle():
    measure = Measure([metric1, metric2], epoch)
    assert measure.get_cycle().df().shape == (13,3)

    mmmffa = Metric(df_mmmffa['MMMFFAQ027S'])
    tb1yr = Metric(df_tb1yr['DTB1YR'])
    measure = Measure([mmmffa, tb1yr])
    assert measure.get_cycle() == None
    measure.set_cycle(epoch)
    assert measure.get_cycle().df().shape == (13,3)

def test_measure_get_interpolated_df():
    measure = Measure([metric1, metric2], epoch)
    assert measure.df().isna().sum().to_list() == [2,1]
    assert measure.df(interpolated=True).isna().sum().to_list() == [0,0]

def test_measure_df_transformations():
    measure = Measure([metric1, metric2], epoch)
    assert measure.to_long().shape == (32,2)
    assert measure.to_long().index.name == 'timestamp'

def test_measure_cycle_transformations():
    measure = Measure([metric1, metric2], epoch)
    result_df = measure.to_long_by_cycle()
    assert result_df.shape == (26,6)
    assert result_df.timestamp.values[0] == np.datetime64('1950-01-01')