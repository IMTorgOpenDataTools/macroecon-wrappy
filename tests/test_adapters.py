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
    YahooFin,
    AlphaVantage,
    InternetArchive
)
from macroecon_wrappy.metric import Metric
from macroecon_wrappy.utils import delete_folder
from macroecon_wrappy.models.classification import classifier

#external
from fredapi import Fred
import yfinance_cache as yfc
from alpha_vantage.timeseries import TimeSeries as avTimeSeries
import waybackpack

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
    metric_from_cache = FredApi.get_data('GDP')
    assert isinstance(metric_from_cache, Metric)
    pop = FredApi.get_data('POPTHM')
    assert isinstance(metric, Metric)

def test_yahoo():
    #setup
    wd = cache_path / 'yfinance'
    delete_folder(wd)
    YahooFin.set_wrapper(auth, yfc)
    #single request
    metrics = YahooFin.get_data(tickers='MSFT')
    metric = metrics['MSFT']
    assert isinstance(metric, Metric)
    assert metric.id == 'MSFT'
    assert metric.title == 'Microsoft Corporation'
    assert metric.shape[0] >= 9655
    metrics1 = YahooFin.get_data(tickers='MSFT', period="max")
    metric1 = metrics1['MSFT']
    assert metric.shape[0] >= metric1.shape[0]
    metrics2 = YahooFin.get_data(tickers='MSFT', start='2020-01-01')
    metric2 = metrics2['MSFT']
    assert metric.shape[0] >= metric2.shape[0]
    metrics3 = YahooFin.get_data(tickers='MSFT', interval="1m")
    metric3 = metrics3['MSFT']
    assert metric3.shape[0] >= 1374
    metric4 = YahooFin.wrapper.download('MSFT', period="1d")
    assert metric4.shape == (1,10)
    metric_from_cache = YahooFin.get_data(tickers='MSFT')
    assert isinstance(metric_from_cache['MSFT'], Metric)
    #batch request
    metrics = YahooFin.get_data(tickers=['MSFT','NVDA'])
    assert metrics['MSFT'].shape[0] > 10000
    assert metrics['NVDA'].shape[0] > 6000

def test_alphavantage():
    wd = cache_path / 'alphavantage'
    delete_folder(wd)
    AlphaVantage.set_wrapper(auth, avTimeSeries)
    metric = AlphaVantage.get_data(tickers='MSFT')
    assert isinstance(metric, Metric)
    del metric
    metric = AlphaVantage.get_data(tickers='MSFT')
    assert metric.id == 'MSFT'     
    assert metric.title == 'MSFT'
    assert metric.shape[0] >= 100

def test_internet_archive():
    """
    example using: `self.wrapper.Asset(url, timestamps[0]).fetch()` 
    https://www.nytimes.com/ => https://web.archive.org/web/19961112181513/http://www.nytimes.com/
    """
    wd = cache_path / 'internet_archive'
    delete_folder(wd)
    InternetArchive.set_wrapper(auth, waybackpack)
    config = {
        'urls':["http://www.bloomberg.com/news/economy/"], 
        'models':[classifier],
        'start': '20080101',
        'end': '20090101',
        'sample': 1,
        }
    event = InternetArchive.get_data(config)
    url = list(event.keys())[0]
    ts = list(event[url].keys())[0]
    assert url == 'http://www.bloomberg.com/news/economy/'
    assert len(str(ts)) == 14
    assert event[url][ts][0]['search'] == 'KW'