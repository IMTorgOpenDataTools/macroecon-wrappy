#!/usr/bin/env python3
"""
test Adapter class and API-wrapper instances
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#wrappy
from macroecon_wrappy.auth import Auth
from macroecon_wrappy.adapters import (
    FredApi,
    YahooFin
)
from macroecon_wrappy.metric import Metric

#external
from fredapi import Fred
import yfinance as yf

#sys
from pathlib import Path



def test_fredapi():
    filepath = Path('SECRETS.yaml')     # <<< must use actual api key
    auth = Auth(filepath)
    auth.load()
    fred = Fred(api_key=auth.data['API_KEY_FED'])

    FredApi.set_wrapper(fred)
    metric = FredApi.get_data('GDP')
    assert isinstance(metric, Metric)
    assert metric.shape[0] >= 313

def test_yahoo():
    YahooFin.set_wrapper(yf)
    metric = YahooFin.get_data(tickers='MSFT')
    assert isinstance(metric, Metric)
    assert metric.shape[0] >= 9655
    metric1 = YahooFin.get_data(tickers='MSFT', period="max")
    assert metric.shape[0] >= metric1.shape[0]
    metric2 = YahooFin.get_data(tickers='MSFT', start='2020-01-01')
    assert metric.shape[0] >= metric2.shape[0]
    metric3 = YahooFin.get_data(tickers='MSFT', interval="1m")
    assert metric3.shape[0] >= 1374
    metric4 = YahooFin.wrapper.download('MSFT', period="1d")
    assert metric4.shape == (1,6)