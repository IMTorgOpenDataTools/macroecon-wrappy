#!/usr/bin/env python3
"""
Tests for plots
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import plotnine as p9

from macroecon_wrappy import plots
from tests.data.test_data import df_series


def test_get_recession_bars():
    bars_df = plots.get_recession_bars()
    assert bars_df.shape[0] == 35

def test_graph_ts():
    plt = plots.graph_ts(df_series, cols=['value1', 'value2'])
    assert type(plt) == p9.ggplot