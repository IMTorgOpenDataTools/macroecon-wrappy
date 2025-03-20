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
    TreasuryFiscal,
    YahooFin,
    InternetArchive
)
from macroecon_wrappy.metric import Metric
from macroecon_wrappy.utils import delete_folder
from macroecon_wrappy.models.classification import classifier

#external
from fredapi import Fred
from treasury.client import FederalTreasuryClient
import yfinance as yf
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
    pop = FredApi.get_data('POPTHM')
    assert isinstance(metric, Metric)


def test_treasury_fiscaldata():
    wd = cache_path / 'treasury_fiscaldata'
    delete_folder(wd)
    TreasuryFiscal.set_wrapper(auth, FederalTreasuryClient)
    assert True == True
    """#TODO: the data appears too dense to place in a simple Metric
    metric = TreasuryFiscal.get_data('other_data-historical_debt_outstanding')
    assert isinstance(metric, Metric)
    assert metric.shape[0] >= 236
    metric = TreasuryFiscal.get_data('public_debt_instruments-details_of_securities_outstanding')
    assert isinstance(metric, Metric)
    assert metric.shape[0] >= 236
    """


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
    assert ts == 20080228084658
    assert event[url][ts][0]['search'] == 'KW'