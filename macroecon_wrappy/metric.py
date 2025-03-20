#!/usr/bin/env python3
"""
Metric class that adds metadata to pd.Series


#TODO: create separate Ticker class for plots to determine candlestick???
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd
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
    
    def normalize_values(self, fun=None):
        """Apply normalization function and get deep, new Metric."""
        def minmax(vec):
            return (vec-vec.min())/(vec.max()-vec.min())

        if not fun:
            fun = minmax
        metric = deepcopy(self)
        new_metric = Metric(fun(metric))
        return new_metric
        