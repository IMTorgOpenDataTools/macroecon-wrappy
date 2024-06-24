#!/usr/bin/env python3
"""
Measure class that combines multiple Metric items.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import pandas as pd


class Measure:
    """A general class to hold many different series of the same measure.
    Example: GDP and GDI are two different timeseries that both measure total
    output of an economy.

    Usage:
        ```
        measure = Measure(df[['GDP','GDI']])
        type(measure.data) == pd.DataFrame
        type(measure.data.index) == "datetime64"
        ```
    Notes:
        - all data must have a `date` index or be a df that includes a column labeled `date`
    TODO:add from notes
    """
    def __init__(self, df_or_series):
        self.data = pd.DataFrame()
        self.add_data(df_or_series)

    def add_data(self, df_or_series):
        """Add data from either DataFrame or Series"""
        df = self.prepare_input_for_ingest(df_or_series)
        #self.data.assign(**df)
        self.data = pd.concat(
            [self.data, df_or_series], 
            axis=1, 
            join='outer'
        )
        
    def prepare_input_for_ingest(self, df_or_series):
        """Check input to ensure it meets required characteristics to 
        be added as data.
        
        Requirements:
            - all data must either be: 
              + Series with `date` (type timeseries) index or 
              + DataFrame that includes a column labeled `date`
            - data columns must be of type float
            - output as DataFrame with timeseries index
        """
        if type(df_or_series)==pd.DataFrame:
            if df_or_series.index.inferred_type == "datetime64":
                return df_or_series
            elif 'date' in df_or_series.columns:
                df_or_series['date'] = pd.to_datetime(df_or_series['date'])
                df_or_series.index = df_or_series['date']
                #df_or_series.drop(labels='date')
                return df_or_series
            else:
                raise Exception()
        elif type(df_or_series)==pd.Series:
            if df_or_series.index.inferred_type == "datetime64":
                df = pd.DataFrame(df_or_series)
                return df
        else:
            raise Exception('arg `df_or_series` must be of type DataFrame or Series')
            
    def to_long(self):
        """Convert data to long-format DataFrame"""
        cols = self.data.columns
        tmp = self.data
        tmp['date'] = df.index
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