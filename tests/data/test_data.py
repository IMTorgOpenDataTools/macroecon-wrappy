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
df_series.index = pd.to_datetime(df_series['date'])

df_cycle = pd.DataFrame([
    {'peak': '1953-07-01', 'trough': '1954-05-01'},
    {'peak': '1957-08-01', 'trough': '1958-04-01'},
    {'peak': '1960-04-01', 'trough': '1961-02-01'},
    {'peak': '1969-12-01', 'trough': '1970-11-01'},
    {'peak': '1973-11-01', 'trough': '1975-03-01'},
    {'peak': '1980-01-01', 'trough': '1980-07-01'},
    {'peak': '1981-07-01', 'trough': '1982-11-01'},
    {'peak': '1990-07-01', 'trough': '1991-03-01'},
    {'peak': '2001-03-01', 'trough': '2001-11-01'},
    {'peak': '2007-12-01', 'trough': '2009-06-01'},
    {'peak': '2020-02-01', 'trough': '2020-04-01'},
])
df_cycle.peak = pd.to_datetime(df_cycle['peak'])
df_cycle.trough = pd.to_datetime(df_cycle['trough'])
