#!/usr/bin/env python3
"""
yahoo finance Adapter 

Note:
* yfinance maintains its own cache
* Use the abstract Adapter methods or access the wrapper directly with: `self.wrapper`
* it is important to note that the 1m (min) data is only retrievable for the last 7 days, 
and anything intraday (interval <1d) only for the last 60 days.
* [yahooquery](https://github.com/dpguthrie/yahooquery) may be a faster alternative
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .adapter import AdapterInterface
from ..metric import Metric

import pandas as pd
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass




class YahooAdapter(AdapterInterface):
    """Interface for wrapper adapter
    
    """

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper and cache."""
        self.wrapper = wrapper
        self.wrapper_name = 'yfinance'
        self.cache_file = auth.cache_path / f"{self.wrapper_name}" / f"{self.wrapper_name}.cache"
        session = CachedLimiterSession(
            limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache(self.cache_file),
        )
        #session.headers['User-agent'] = 'my-program/1.0'
        self.session = session
        self._set_cache_path(auth, self.wrapper_name)
        

    def get_data(self, **kwargs):
        """Get average (high, low) data from API and return object of class Metric.
        
        start, end: "2022-01-01"
        period: 'max'
        interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

        Note: to get all ticker data, such as for a candlestick, use the 
        self.wrapper, direcetly:
            >>> YahooFin.self.wrapper.download(tickerId, period="max", session=self.session)
        """
        tickerId = kwargs['tickers']
        tkr = self.wrapper.Ticker(tickerId, session=self.session)
        try:
            if list(kwargs.items()).__len__()==1:
                df_hist = self.wrapper.download(tickerId, period="max", session=self.session)
            else:
                df_hist = self.wrapper.download(**kwargs, session=self.session)
            '''
            #TODO:add
            tkr.get_shares_full(start=start_date, end=end_date)
            tkr.msft.actions
            tkr.msft.dividends
            tkr.splits
            tkr.capital_gains
            '''
        except Exception as e:
            print(e)
        ts = df_hist[['High', 'Low']].mean(axis=1)

        #TODO: metadata mapping needs improvement
        metric = Metric(ts)
        metric.title = tkr.info['longName']
        metric.id = tkr.info['symbol']
        metric.source = 'finance.yahoo.com/'
        metric.references = None
        metric.notes = None
        metric.date_range = df_hist.index.min(), df_hist.index.max()
        metric.frequency = None
        metric.last_updated = None
        metric.obseravation_date = None
        metric.release = None
        metric.seasonal_adjustment = None
        metric.seasonal_adjustment_short = None
        metric.t = df_hist.index.max() - df_hist.index.min()
        metric.units = '$ - dollar'
        metric.units_short = '$'

        metric.set_metadata(**tkr.info)
        return metric
    
    def _set_cache_path(self, auth, name):
        """Set the directory (and file) to use as cache."""
        cache_path = auth.cache_path / name
        cache_path.mkdir(parents=False, exist_ok=True)
        self.wrapper.set_tz_cache_location(cache_path)

    def _cache_data(self, key, data):
        """Save data to cache."""
        raise NotImplementedError("Cache maintained with API-wrapper")

    def _get_data_if_cached(self, key):
        """Check if data is cached and retrieve if so."""
        raise NotImplementedError("Cache maintained with API-wrapper")