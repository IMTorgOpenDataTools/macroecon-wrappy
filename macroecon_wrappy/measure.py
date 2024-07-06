#!/usr/bin/env python3
"""
Measure class that combines multiple Metric items.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .metric import Metric

import pandas as pd


class Measure:
    """A general class to hold many different series of the same measure.
    Example: GDP and GDI are two different timeseries that both measure total
    output of an economy.

    Usage:
        ```
        metrics = [gdp, gdi]
        measure = Measure(metrics)
        type(measure.df()) == pd.DataFrame
        type(measure.df().index) == "datetime64"
        ```
    Notes:
        - all data must be of type `Metric` with a `pd.Timestamp` index
    """
    def __init__(self, metric_or_metric_list):
        self.metrics = []
        self.add_metric(metric_or_metric_list)

    def add_metric(self, metric_or_metric_list):
        """Add data from either Metric or list of Metrics"""
        metric_list = self.prepare_input_for_ingest(metric_or_metric_list)
        self.metrics.extend(metric_list)
        
    def prepare_input_for_ingest(self, metric_or_metric_list):
        """Check input to ensure it meets required characteristics to 
        be added as data.
        
        TODO:put into Metric
        Requirements:
            - all data must either be: 
              + Series with `date` (type timeseries) index or 
              + DataFrame that includes a column labeled `date`
            - data columns must be of type float
            - output as DataFrame with timeseries index
        """
        data = metric_or_metric_list
        if isinstance(data, Metric):
            return [data]
        elif isinstance(data, list):
            for item in data:
                assert isinstance(item, Metric)
            return data
        else:
            raise Exception('arg `metric_or_metric_list` must be of type Metric of list of Metrics')
        
    def df(self):
        return pd.DataFrame(self.metrics)
            
    def to_long(self):
        """Convert data to long-format DataFrame"""
        cols = self.df().columns
        tmp = self.df()
        tmp['date'] = tmp.index
        tmp.reset_index(drop=True, inplace=True)
        tmp = pd.melt(tmp, id_vars='date', value_vars=cols, var_name='grp', value_name='value')
        return tmp

    def to_long_by_cycle(self):
        """Convert to long-format separated by the business cycle"""
        #TODO
        return True


    def set_metadata(self):
        """Set metadata on Series"""
        #TODO
        return True