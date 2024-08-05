#!/usr/bin/env python3
"""
Measure class that combines multiple Metric items.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .metric import Metric
from .epoch import Epoch

import pandas as pd
import numpy as np

from copy import deepcopy


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
    def __init__(self, metric_or_metric_list, cycle_epoch=None):
        self.metrics = []
        self.cycle = pd.DataFrame()
        self.add_metric(metric_or_metric_list)
        if cycle_epoch:
            self.set_cycle(cycle_epoch)

    def __repr__(self) -> str:
        """Return a string representation."""
        return self.df().head().__repr__()

    def add_metric(self, metric_or_metric_list):
        """Add data from either Metric or list of Metrics."""
        metric_list = self.prepare_input_for_ingest(metric_or_metric_list)
        result_metrics = [Metric(metric.sort_index(ascending=False)) for metric in metric_list]
        self.metrics.extend(result_metrics)

    def get_metric(self, metric_lst=[]):
        """Return a specific metric or all metrics (if metric is None)."""
        if not isinstance(metric_lst, list):
            raise Exception('metric must be of type list')
        if len(metric_lst)==0:
            return self.metrics
        elif len(metric_lst)>0:
            result_metrics = [Metric(metric.sort_index(ascending=False)) for metric in self.metrics if metric in metric_lst]
            return result_metrics

    def set_cycle(self, cycle_epoch):
        """Set the default cycle for transformations."""
        if isinstance(cycle_epoch, Epoch):
            self.cycle = cycle_epoch
        else:
            raise Exception('arg `cycle_epoch` must be of type Epoch')
        
    def get_cycle(self):
        """..."""
        if self.cycle:
            return self.cycle
        else:
            raise Exception('no self.cycle of `Epoch` is available.  use measure.set_cycle(cycle)')
        
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
        """Get combined pd.DataFrame of Metrics, Cycle, etc."""
        df = pd.DataFrame(self.metrics).transpose()
        #df.columns = [metric.id if (metric.id not in [None, '']) else f'col-{idx}' for idx, metric in enumerate(self.metrics) ]
        df.columns = [metric.id if (hasattr(metric, 'id') and getattr(metric, 'id') not in [None, '']) else f'col-{idx}' for idx, metric in enumerate(self.metrics) ]
        df.sort_index(ascending=False, inplace=True)
        return df
    
    def subset_by_time(self, start, end):
        """Subset the Metrics by start, end Timestamps to produce new Measure."""
        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        #msk = (self.df().index > start) & (self.df().index < end)
        results = []
        for metric in self.metrics:
            metric.sort_index(ascending=False, inplace=True)
            msk = (metric.index > start) & (metric.index < end)
            new_metric = Metric(metric[msk])
            if new_metric.shape[0]>0:
                results.append( new_metric )
        measure = Measure(results)
        return measure

    def to_long(self):
        """Convert data to long-format DataFrame."""
        cols = self.df().columns
        tmp = self.df()
        tmp.reset_index(inplace=True)
        tmp = pd.melt(tmp, id_vars='timestamp', value_vars=cols, var_name='grp', value_name='value')
        tmp.set_index('timestamp', inplace=True)
        return tmp

    def to_long_by_cycle(self, cycle=None):
        """Get list of pd.DataFrames separated by the business cycles."""
        if not cycle:
            if self.cycle:
                cycle = self.cycle
            else:
                raise Exception('no cycle provided')
        results = []
        for idx,event in enumerate(cycle.get_items()):
            event = deepcopy(event)
            if idx==0:
                start = pd.to_datetime(self.df().index).min()
            event.start = start
            #subset index by cycle start,end
            subset_measure = self.subset_by_time(event.start, event.end)
            if len(subset_measure.get_metric())==0:
                pass
            else:
                #normalize(0,1) each column
                normalized_metrics = [metric.normalize_values() for metric in subset_measure.get_metric()]
                normalized_subset_long = Measure(normalized_metrics).to_long()
                #normalize x-axis
                normalized_subset_long.reset_index(inplace=True)
                normalized_subset_long['timestamp']  = pd.to_datetime(normalized_subset_long['timestamp'] )
                normalized_subset_long['start']  = pd.to_datetime( event.start )
                normalized_subset_long['diff_days'] = (normalized_subset_long['timestamp']-normalized_subset_long['start']).dt.days.astype('int')
                normalized_subset_long['end'] =  pd.to_datetime( event.end )
                normalized_subset_long['end'] = (normalized_subset_long['end'] - normalized_subset_long['start']).dt.days.astype('int')
                normalized_subset_long['diff_pct'] = np.where(
                    normalized_subset_long['diff_days'] < 1, 
                    normalized_subset_long['diff_days'], 
                    normalized_subset_long['diff_days'] / normalized_subset_long['end']
                )
                #wrap-up
                normalized_subset_long.drop(labels=['start','end'], axis=1, inplace=True)
                normalized_subset_long['cycle'] = event.name
                results.append(normalized_subset_long)
            start = event.end
        result_df = pd.concat(results, axis=0)
        return result_df


    def set_metadata(self):
        """Set metadata on Series"""
        #TODO
        return True