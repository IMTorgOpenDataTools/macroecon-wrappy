#!/usr/bin/env python3
"""
Tests loading data using requests to sources
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from macroecon_wrappy.load import (
    get_most_popular_series
)


def test_get_most_popular_series_fred():  
    N = 10
    seriesIds = get_most_popular_series(N, 'fred')
    assert seriesIds.__len__() == N