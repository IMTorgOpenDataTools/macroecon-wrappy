#!/usr/bin/env python3
"""
Tests data for all tests
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd



#test data
df_series = pd.DataFrame([
    {'date': '1940-01-01', 'value1': 200.0, 'value2': 300},
    {'date': '1950-01-01', 'value1': 300.0, 'value2': 600},
    {'date': '1960-01-01', 'value1': 400.0, 'value2': 800},
    {'date': '1970-01-01', 'value1': 700.0, 'value2': 700},
    {'date': '1980-01-01', 'value1': 800.0, 'value2': 900},
    {'date': '1990-01-01', 'value1': 1000.0, 'value2': 950},
])
df_series['date'] = pd.to_datetime(df_series['date'])