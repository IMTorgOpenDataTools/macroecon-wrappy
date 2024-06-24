#!/usr/bin/env python3
"""
test Measure class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.measure import Measure
from tests.data.test_data import df_series

import pandas as pd



def test_measure():
    measure = Measure(df_series)
    assert type(measure.data) == pd.DataFrame
    assert type(measure.data.index) == pd.core.indexes.datetimes.DatetimeIndex