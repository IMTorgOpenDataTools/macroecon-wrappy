#!/usr/bin/env python3
"""
Metric class that adds metadata to pd.Series


#TODO: create separate Ticker class for plots to determine candlestick???
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize

from copy import deepcopy

class Metric(pd.Series):
    """Series object with meta-data.

    Series
        * index: (Timestamp)
        * values: (float)

    Metadata    #TODO: infer most of these and require timeseries index
        * date_range: (string) - specifies the dates of the first and last observations.
        * frequency: (string) - data frequency. `Daily`, `Weekly`, `Monthly`, `Quarterly`, `Semiannual`, or `Annual`.
        * frequency_short: (string) - data frequency. Abbreviated. `D`, `W`, `M`, `Q`, `SA, or `A`.
        * last_updated: (string) - date series was last updated.
        * notes: (string) - details about series. Not available for all series.
        * observation_date: (string) - vintage date at which data are observed.
        * release: (string) - statistical release containing data.
        * seasonal_adjustment: (string) - specifies whether the data has been seasonally adjusted.
        * seasonal_adjustment_short: (string) - specifies whether the data has been seasonally adjusted. Abbreviated.
        * series_id: (string) - unique FRED series ID code.
        * source: (string) - original source of the data.
        * t: (int) - number corresponding to frequency: 365 for daily, 52 for weekly, 12 for monthly, 4 for quarterly, and 1 for annual.
        * title: (string) - title of the data series.
        * units: (string) - units of the data series.
        * units_short: (string) - units of the data series. Abbreviated.
    """

    def __init__(self, data):
        super().__init__(data=data)
        self._metadata = {}
        
        self.title = None
        self.id = None
        self.source = None
        self.references = None
        self.notes = None
        self.date_range = None
        self.frequency = None
        self.last_updated = None
        self.obseravation_date = None
        self.release = None
        self.seasonal_adjustment = None
        self.seasonal_adjustment_short = None
        self.t = None
        self.units = None
        self.units_short = None

        self.index.set_names(['timestamp'], inplace=True)

    def __repr__(self):
        return super().__repr__()
    
    """
    def __getstate__(self):
        state = self.__dict__.copy()
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
    """
    def set_metadata(self, **kwargs):
        """Set metadata for the Metric.
        
        TODO: 
          - currently, when a pd.Series method is called, it returns a pd.Series
          - instead, apply a decorator to each method, here, so that the decorator will return the pd.Series as a Metric
          - ref: https://stackoverflow.com/questions/2998969/how-to-make-every-class-method-call-a-specified-method-before-execution?rq=3
        """
        for key, value in kwargs.items():
            if key in dir(self):
                setattr(self, key, value)
            self._metadata[key] = value

    def get_metadata(self):
        """Get metadata."""
        return self._metadata
    
    def change_time(self, rule='M'):
        """Change time frequency

        rules:
            * T or min: Minute
            * H: Hour
            * D: Day
            * B: Business day
            * W: Week
            * M: Month end
            * MS: Month start
            * Q: Quarter end
            * A or Y: Year end 

        Key Parameters
            * rule: The frequency string (e.g.'5min''2S').
            * closed: Which side of the interval is closed ('left' or 'right').
            * label: Which bin edge label to use ('left' or 'right').
        TODO: use mean or closing?
        """
        result  = self.resample(rule).mean()
        result = Metric(result)
        return result 

    def normalize_values(self, fun=None):
        """Apply normalization function and get new (deep copy) Metric.
        
        """
        def minmax(vec):
            return (vec-vec.min())/(vec.max()-vec.min())

        if not fun:
            fun = minmax
        result = Metric(fun(self))
        return result
    
    def returns(self, type='simple', days=252):
        """
        Get a variety of metric returns
        
        :param type: type of returns requested, in 'simple', 'cumulative', 'log', 'annualized'
        :param days: (trading days) typically used to annualize return when metric values are daily
        """
        type_options = ['simple', 'cumulative', 'log', 'annualized']
        result = None
        timeframe_return = self.pct_change()   #typically used with `data['Adj Close']` 
        if type==type_options[0]:
            result = timeframe_return
        elif type==type_options[1]:
            cumulative_return = (1 + timeframe_return).cumprod()
            result = cumulative_return
        elif type==type_options[2]:
            log_return = np.log(self.values / self.shift(1))
            result = log_return
        elif type==type_options[3]:
            annual_return = timeframe_return.mean() * days
            result = annual_return
        result = Metric(result)
        return result
    
    def ema(self, span=20, adjust=False):
        """
        Calculate EMA using pandas ewm()
        Note:
            typically one usses 'Close'
            span: corresponds to the N-day EMA
            adjust=False: ensures the formula uses the recursive formula: EMA_t = alpha*x_t + (1-alpha)*EMA_{t-1}
        
        Key Considerations
            * EMA Formula: The .ewm() method uses the formula, above 
            * Adjust Parameter: Using adjust=False provides a more consistent, recursive EMA calculation, which is preferred for technical analysis.
            * Window Size: Common EMAs include 9, 12, 26, 50, and 200 days.
            * Handling NaNs: The first few values will be equivalent to a Simple Moving Average (SMA) or NaN depending on how the calculation is initialized, as it needs previous data to establish the first EMA point. 
        """
        ema = self.ewm(span=span, adjust=adjust).mean()
        result = Metric(ema)
        return result

    def moment_values(self, type='EMA', window=21, trading_days=252):
        """
        Get metric's moment values, such as
        * Exponential Moving Avg
        * Volatility
        * etc.

        :param type <'VOL','SKW','KUR'>: 
        :param trading_days=252 annualizes the values

        Usage
            * Log returns with `metric1.returns(type='log')` are preferred for volatility because they are additive
            * Often use 21-day (approx. one trading month) window as an example for monthly volatility
            * 252 is the typical number of trading days in a year
        """
        type_mapping = {
            'VOL':{
                'type':'volatility',
                'function': 'std',
                'exponent': 1/2,
            },
            'SKW':{
                'type':'skew',
                'function': 'skew',
                'exponent': 1/3,
            },
            'KUR':{
                'type':'kurtosis',
                'function': 'kurtosis',
                'exponent': 1/4,
            },
        }
        metric = self
        if trading_days:
            if len(metric) < trading_days:
                return None
        else:
            trading_days = self.shape[0]
        func = type_mapping[type]['function']
        exponent = type_mapping[type]['exponent']
        result = getattr(metric.rolling(window=window), func)() * np.power(trading_days, exponent)
        result = Metric(result)
        return result