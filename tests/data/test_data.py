#!/usr/bin/env python3
"""
Tests data for all tests
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd
import numpy as np

from pathlib import Path



#test data
df_series = pd.DataFrame([
    {'date': '1940-01-01', 'value1': 200.0, 'value2': 300},
    {'date': '1950-01-01', 'value1': 300.0, 'value2': 600},
    {'date': '1960-01-01', 'value1': 400.0, 'value2': 800},
    {'date': '1963-01-01', 'value1': 400.0, 'value2': 800},
    {'date': '1963-06-01', 'value1': 300.0, 'value2': 700},
    {'date': '1964-01-01', 'value1': 500.0, 'value2': np.nan},
    {'date': '1965-01-01', 'value1': np.nan, 'value2': 800},
    {'date': '1970-01-01', 'value1': 700.0, 'value2': 700},
    {'date': '1980-01-01', 'value1': 800.0, 'value2': 900},

    {'date': '1981-01-01', 'value1': 900.0, 'value2': 600},
    {'date': '1982-01-01', 'value1': 400.0, 'value2': 500},
    {'date': '1984-01-01', 'value1': np.nan, 'value2': 800},
    {'date': '1986-01-01', 'value1': 800.0, 'value2': 300},
    {'date': '1987-01-01', 'value1': 900.0, 'value2': 500},
    {'date': '1988-01-01', 'value1': 800.0, 'value2': 900},

    {'date': '1990-01-01', 'value1': 1000.0, 'value2': 950},
])
df_series.index = pd.to_datetime(df_series['date'])

df_cycle = pd.DataFrame([
    {'peak': '1953-07-01', 'trough': '1954-05-01', 'name': 'recession1'},
    {'peak': '1957-08-01', 'trough': '1958-04-01', 'name': 'recession2'},
    {'peak': '1960-01-01', 'trough': '1960-01-01', 'name': 'shock'},
    {'peak': '1960-04-01', 'trough': '1961-02-01', 'name': 'recession3'},
    {'peak': '1969-12-01', 'trough': '1970-11-01', 'name': 'recession4'},
    {'peak': '1973-11-01', 'trough': '1975-03-01', 'name': 'recession5'},
    {'peak': '1980-01-01', 'trough': '1980-07-01', 'name': 'recession6'},
    {'peak': '1981-07-01', 'trough': '1982-11-01', 'name': 'recession7'},
    {'peak': '1990-01-01', 'trough': '1990-01-01', 'name': 'shock'},
    {'peak': '1990-07-01', 'trough': '1991-03-01', 'name': 'recession8'},
    {'peak': '2001-03-01', 'trough': '2001-11-01', 'name': 'recession9'},
    {'peak': '2007-12-01', 'trough': '2009-06-01', 'name': 'recession10'},
    {'peak': '2020-02-01', 'trough': '2020-04-01', 'name': 'recession11'},
])
df_cycle.peak = pd.to_datetime(df_cycle['peak'])
df_cycle.trough = pd.to_datetime(df_cycle['trough'])



filepath = Path('./tests/data/fred/MMMFFAQ027S.csv')
df_mmmffa = pd.read_csv(filepath)
df_mmmffa.set_index('observation_date', inplace=True)

filepath = Path('./tests/data/fred/DTB1YR.csv')
df_tb1yr = pd.read_csv(filepath)
df_tb1yr.set_index('observation_date', inplace=True)