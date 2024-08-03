#!/usr/bin/env python3
"""
Metric class that adds metadata to pd.Series
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd


class Metric(pd.Series):
    """Series object with meta-data.

    Series
        * index: (Timestamp)
        * values: (float)

    Metadata
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
        for key, value in kwargs.items():
            if key in dir(self):
                setattr(self, key, value)
            self._metadata[key] = value

    def get_metadata(self):
        return self._metadata