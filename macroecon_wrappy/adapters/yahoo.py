#!/usr/bin/env python3
"""
yahoo finance Adapter 

Note:
* yfinance_cache maintains its own cache
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
from .. import utils

import pandas as pd
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket, LimiterSession
from pyrate_limiter import Duration, RequestRate, Limiter

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

import time
import json




class YahooAdapter(AdapterInterface):
    """Interface for wrapper adapter
    
    """

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper and cache."""
        self.wrapper = wrapper
        self.wrapper_name = 'yfinance'
        self.cache_file = auth.cache_path / f"{self.wrapper_name}" / f"{self.wrapper_name}.cache"
        #TODO:effectively implement yfinance_cache
        '''
        history_rate = RequestRate(1, Duration.SECOND) 
        limiter = Limiter(history_rate)
        session = LimiterSession(limiter=limiter)
        session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        
        session = CachedLimiterSession(
            limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache(self.cache_file),
        )
        session.headers['User-agent'] = 'my-program/1.0'
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

        def metric_factory(ts, tkr=None, df_hist=None):
            """..."""
            metric = Metric(ts)
            if tkr:
                metric.title = tkr.info['longName']
                metric.id = tkr.info['symbol']
                metric.set_metadata(**tkr.info)
            else:
                metric.title = None
                metric.id = None
            metric.source = 'finance.yahoo.com/'
            metric.references = None
            metric.notes = None
            if df_hist.shape[0] > 0:
                metric.date_range = df_hist.index.min(), df_hist.index.max()
                metric.t = df_hist.index.max() - df_hist.index.min()
            else:
                metric.date_range = None, None
                metric.t = None
            metric.frequency = None
            metric.last_updated = None
            metric.obseravation_date = None
            metric.release = None
            metric.seasonal_adjustment = None
            metric.seasonal_adjustment_short = None
            metric.units = '$ - dollar'
            metric.units_short = '$'
            return metric
        
        def get_data_for_single_ticker(ticker):
            """
            Note: metadata requested
            """
            results = {}
            tkr = self.wrapper.Ticker(ticker)
            time.sleep(1)#TODO:anything more pythonic?
            df_hist = self.wrapper.download(ticker, period="max")
            time.sleep(1)
            tmp1 = utils.filter_nested_dict(tkr.__dict__, utils.criteria_func)
            tmp2 = utils.serialize_dir(tkr)
            tmp2.update(tmp1)
            #attrs = json.dumps(tmp2)#, default=utils.replace_non_serializable)
            data = {
                'df': df_hist,
                'tkr': tmp2
                }
            self._cache_data(ticker, data)
            data['tkr'] = tkr
            results[ticker] = data
            return results
        
        def get_data_for_multiple_tickers(tickers):
            """
            Note: no metadata requested
            """
            results = {}
            df_multi_index = self.wrapper.download(tickers, period="max")
            dfs = utils.separate_batch_call_to_dict_of_dfs(df_multi_index )
            time.sleep(1)
            for tkr, df_hist in dfs.items():
                data = {
                    'df': df_hist,
                    'tkr': None
                    }
                self._cache_data(tkr, data)
                results[tkr] = data
            return results
        
        #check if available in cache
        def check_retrieve_from_cache(ticker_list):
            """..."""
            missing_data = {}
            available_data = {}
            for ticker in ticker_list:
                data = self._get_data_if_cached(key=ticker)
                if data:
                    tkr = self.wrapper.Ticker(ticker)
                    if 'tkr' in data:
                        for key, value in data['tkr'].items():
                            try:
                                setattr(tkr, key, value)
                            except:
                                pass
                        data['tkr'] = tkr
                    available_data[ticker] = data
                else:
                    missing_data[ticker] = None
            return available_data, missing_data
        
        #main
        tickerIds = kwargs['tickers']
        if type(tickerIds) == str:
            tickerIds = [tickerIds]
        #cache
        available_data, missing_data = check_retrieve_from_cache(tickerIds)
        #o/w get data
        if missing_data:
            try:
                if len(missing_data.keys()) == 1:
                    ticker = list(missing_data.keys())[0]
                    more_available_data = get_data_for_single_ticker(ticker)
                else:
                    more_available_data = get_data_for_multiple_tickers(missing_data.keys())
                available_data.update(more_available_data)
            except Exception as e:
                print(e)
        metrics = {}
        for symbol, data in available_data.items():
            ts = data['df'][['High', 'Low']].mean(axis=1)
            metric = metric_factory(ts, tkr=data['tkr'], df_hist=data['df'])    #tkr=data['tkr'] ?whats wrong
            metrics[symbol] = metric
        return metrics
    
    '''
    def _set_cache_path(self, auth, name):
        """Set the directory (and file) to use as cache.
        TODO:maybe use yfinance-specific cache later
        """
        cache_path = auth.cache_path / name
        cache_path.mkdir(parents=False, exist_ok=True)
        self.wrapper.set_tz_cache_location(cache_path)
    '''