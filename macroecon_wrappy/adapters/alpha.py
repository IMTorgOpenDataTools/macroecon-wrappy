#!/usr/bin/env python3
"""
alpha vantage Adapter 


TODO: update with yahoo.py structure

Note:
* [alpha_vantage](https://github.com/RomelTorres/alpha_vantage)
* Use the abstract Adapter methods or access the wrapper directly with: `self.wrapper`
* limited 25 requests per day, 5 requests per minute, outputsize='compact' is 100 days of data
* [API reference](https://www.alphavantage.co/documentation/#intraday)
* [FAQ](https://www.alphavantage.co/support/#api-key)
* alternative is [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/pricing)
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




class AlphaVantageAdapter(AdapterInterface):
    """Interface for wrapper adapter
    
    """

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper and cache."""
        self.wrapper = wrapper(key=auth.data['API_KEY_ALPHA'], output_format='pandas', indexing_type='date')
        self.wrapper_name = 'alphavantage'
        self.cache_file = auth.cache_path / f"{self.wrapper_name}" / f"{self.wrapper_name}.cache"
        '''
        session = CachedLimiterSession(
            limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache(self.cache_file),
        )
        #session.headers['User-agent'] = 'my-program/1.0'
        self.session = session
        '''
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

        #check if already available
        data = self._get_data_if_cached(key=tickerId)
        if data:
            df_hist = data['df']
            meta_data = data['meta']
        else:
            #otherwise get data
            try:
                if list(kwargs.items()).__len__()==1:
                    df_hist, meta_data = self.wrapper.get_daily(tickerId, outputsize='compact')
                else:
                    df_hist, meta_data = self.wrapper.download(**kwargs, outputsize='compact')
                data = {
                    'df': df_hist,
                    'meta': meta_data
                }
                self._cache_data(tickerId, data)
            except Exception as e:
                print(e)
        df_ts = df_hist.rename(columns={
            '1. open':'Open', 
            '2. high':'High', 
            '3. low':'Low', 
            '4. close':'Close', 
            '5. volume':'Volume'
        })
        ts = df_ts[['High', 'Low']].mean(axis=1)
        
        #metadata mapping
        metric = Metric(ts)
        metric.title = meta_data['2. Symbol']
        metric.id = meta_data['2. Symbol']
        metric.source = 'alphavantage.co/'
        metric.references = None
        metric.notes = meta_data['1. Information']
        metric.date_range = df_ts.index.min(), df_ts.index.max()
        metric.frequency = None
        metric.last_updated = meta_data['3. Last Refreshed']
        metric.obseravation_date = None
        metric.release = None
        metric.seasonal_adjustment = None
        metric.seasonal_adjustment_short = None
        metric.t = df_ts.index.max() - df_ts.index.min()
        metric.units = '$ - dollar'
        metric.units_short = '$'
        #metric.set_metadata(**meta_data.info)
        '''
        #TODO:add
        tkr.get_shares_full(start=start_date, end=end_date)
        tkr.msft.actions
        tkr.msft.dividends
        tkr.splits
        tkr.capital_gains
        '''

        return metric
    
    '''
    def _set_cache_path(self, auth, name):
        """Set the directory (and file) to use as cache.
        TODO:maybe use yfinance-specific cache later
        """
        cache_path = auth.cache_path / name
        cache_path.mkdir(parents=False, exist_ok=True)
        self.wrapper.set_tz_cache_location(cache_path)
    '''