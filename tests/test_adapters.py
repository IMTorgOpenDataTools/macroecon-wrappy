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
from macroecon_wrappy.utils import delete_folder

#external
from fredapi import Fred
import yfinance as yf

#sys
from pathlib import Path



#setup
secrets_path = Path('SECRETS.yaml')     # <<< must use actual api key
cache_path = Path('./tests/tmp')
auth = Auth(secrets_path, cache_path)
auth.load_secrets()


def test_fredapi():
    wd = cache_path / 'fredapi'
    delete_folder(wd)
    FredApi.set_wrapper(auth, Fred)
    metric = FredApi.get_data('GDP')
    assert isinstance(metric, Metric)
    assert metric.shape[0] >= 313
    assert metric.title == 'Gross Domestic Product'

def test_yahoo():
    wd = cache_path / 'yfinance'
    delete_folder(wd)
    YahooFin.set_wrapper(auth, yf)
    metric = YahooFin.get_data(tickers='MSFT')
    assert isinstance(metric, Metric)
    assert metric.id == 'MSFT'
    assert metric.title == 'Microsoft Corporation'
    assert metric.shape[0] >= 9655
    metric1 = YahooFin.get_data(tickers='MSFT', period="max")
    assert metric.shape[0] >= metric1.shape[0]
    metric2 = YahooFin.get_data(tickers='MSFT', start='2020-01-01')
    assert metric.shape[0] >= metric2.shape[0]
    metric3 = YahooFin.get_data(tickers='MSFT', interval="1m")
    assert metric3.shape[0] >= 1374
    metric4 = YahooFin.wrapper.download('MSFT', period="1d")
    assert metric4.shape == (1,6)