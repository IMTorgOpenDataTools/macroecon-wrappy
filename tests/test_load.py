#!/usr/bin/env python3
"""
Tests loading data using requests to sources
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from macroecon_wrappy.load import (
    get_most_popular_series,
    get_recession_bars
)


def test_get_most_popular_series_fred():  
    N = 10
    seriesIds = get_most_popular_series(N, 'fred')
    assert seriesIds.__len__() == N

def test_get_recession_bars():
    bars_df = get_recession_bars()
    assert bars_df.shape[0] == 35