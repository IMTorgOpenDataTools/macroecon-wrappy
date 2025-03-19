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
    measure = Measure([metric1, metric2])
    assert isinstance(measure.df(), pd.DataFrame)
    assert measure.df().shape == (16,2)
    results = []
    for idx, name in enumerate(['col-0', 'col-1']):
        result = measure.df().columns[idx]==name
        results.append(result)
    assert all(results)
    assert isinstance(measure.df().index, pd.core.indexes.datetimes.DatetimeIndex)
    measure = Measure([metric1, metric2], epoch)
    assert measure.df().shape == (16,2)
    assert measure.get_cycle().df().shape == (13,3)

def test_measury_get_cycle():
    measure = Measure([metric1, metric2], epoch)
    assert measure.get_cycle().df().shape == (13,3)

    mmmffa = Metric(df_mmmffa['MMMFFAQ027S'])
    tb1yr = Metric(df_tb1yr['DTB1YR'])
    measure = Measure([mmmffa, tb1yr])
    assert measure.get_cycle() == None
    measure.set_cycle(epoch)
    assert measure.get_cycle().df().shape == (13,3)

    


def test_measure_transformations():
    measure = Measure([metric1, metric2], epoch)
    measure.to_long()
    assert measure.to_long().shape == (12,2)
    assert measure.to_long().index.name == 'timestamp'

def test_measure_cycle_transformations():
    measure = Measure([metric1, metric2], epoch)
    result_df = measure.to_long_by_cycle()
    assert result_df.shape == (26,6)
    assert result_df.timestamp.values[0] == np.datetime64('1950-01-01')