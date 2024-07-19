#!/usr/bin/env python3
"""
Epoch class that combines multiple Event items.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#from .span import Span

import pandas as pd
import numpy as np
from datetime import datetime


class Event:
    """..."""

    def __init__(self, event):
        self.value = event


class Span:
    """..."""

    def __init__(self, span):
        self.value = span


def epoch_row_factory(row):
    """Factor for creating Span or Event from Epoch row."""
    diff = row[Epoch._names[1]] == row[Epoch._names[0]]
    if diff >= Epoch._determine_event_duration_cutoff:
        return Event(row)
    else:
        return Span(row)
    



class Epoch:
    """..."""

    def __init__(self, df_or_list):
        self._names = ['start', 'end']
        self._span_duration_seconds = 0
        self._determine_event_duration_cutoff = 0
        mod_df = self.prepare_input_for_ingest(df_or_list)
        self.df_data = mod_df

    def __repr__(self) -> str:
        """Return a string representation."""
        return self.df().__repr__()
    
    def prepare_input_for_ingest(self, df_or_list):
        """Check input to ensure it meets required characteristics to 
        be added as data.

        #TODO: add i) non-overlapping dates, ii) name column possible, ???
        """
        #support function
        def diff_between_events(row):
            """Get difference in time between consecutive events"""
            idx = row.idx
            if idx + 1 < df.shape[0]:
                current = df.iloc[idx]
                next = df.iloc[idx+1]
                consecutive_event_diff_secs = (next[self._names[0]] - current[self._names[1]]).total_seconds()
                return consecutive_event_diff_secs
            else:
                return pd.NaT

        #check datatype
        if isinstance(df_or_list, list):
            df = pd.DataFrame(df_or_list)
        else:
            df = df_or_list
        if not isinstance(df, pd.core.frame.DataFrame):
            raise Exception('arg `df_or_list` must be of type pd.DataFrame or a list of dicts convertible to a DataFrame')
        #check attributes
        if not df.shape[0] >= 1 and df.shape[1] >= 2:
            raise Exception('arg `df` must be of type pd.DataFrame with at least 1 row and two columns')
        if not list(df.columns) == self._names:
            print(f'first two columns will be renamed: {self._names}')
            for idx, col in enumerate(df.columns):
                colname = self._names[idx]
                df.rename(columns={ col: colname }, inplace = True)
                df[colname] = pd.to_datetime(df[colname])
        #reset config
        df.reset_index(
            drop=True, 
            inplace=True
            )
        df.sort_values(
            by=self._names[0], 
            inplace=True
            )
        #check within event times
        diff_within_event_sec = (df[self._names[1]] - df[self._names[0]]).dt.seconds
        dt_out_of_order_within_rows = diff_within_event_sec[diff_within_event_sec < self._span_duration_seconds]
        if len(dt_out_of_order_within_rows) > 0:
            raise Exception(f'all rows of column {self._names[1]} must be temporarily after {self._names[0]} by at least {self._span_duration_seconds} sec.  the following indices do not meet this requirements {dt_out_of_order_within_rows.indices.to_list()}')
        #check between event times
        index_name = 'idx'
        df[index_name] = range(0, df.shape[0])
        diff_between_events_sec = df.apply(diff_between_events, axis=1)
        df.drop(labels=index_name, inplace=True, axis=1)
        dt_out_of_order_between_rows = diff_between_events_sec[diff_between_events_sec < self._span_duration_seconds]
        if len(dt_out_of_order_between_rows) > 0:
            raise Exception(f'all consecutive rows of column {self._names[1]} must be temporarily after {self._names[0]} by at least {self._span_duration_seconds} sec.  the following indices do not meet this requirements {dt_out_of_order_between_rows.indices.to_list()}')
        return df

    def df(self, dates_only=False):
        """Get underlying data as pd.DataFrame"""
        if dates_only:
            return self.df_data[self._names]
        else:
            return self.df_data
        
    def idx(self, idx_or_date):
        """Get selected row as Event."""
        row = None
        if isinstance(idx_or_date, int):
            idx = idx_or_date
            row = self.df().iloc[idx]
        elif isinstance(idx_or_date, datetime):
            dt = idx_or_date
            colnames = self._names
            df = self.df()
            row = df[ (df[colnames[0]] < dt) & (df[colnames[1]] > dt) ]
        elif isinstance(idx_or_date, str):
            try:
                dt_str = idx_or_date
                dt = datetime.strptime(dt_str, '%Y-%m-%d')
            except Exception as e:
                print(f'arg {dt_str} is of type `str` but cannot be converted to datetime')
                print(e)
            colnames = self._names
            df = self.df()
            row = df[ (df[colnames[0]] < dt) & (df[colnames[1]] > dt) ]
        #TODO: determine event or span
        item_event_or_span = epoch_row_factory(row)
        return item_event_or_span
        
    def to_long(self):
        """Convert data to long-format DataFrame"""
        cols = self._names
        tmp = self.df(dates_only=True)
        tmp['date'] = tmp.index
        tmp.reset_index(drop=True, inplace=True)
        tmp = pd.melt(tmp, id_vars='date', value_vars=cols, var_name='grp', value_name='value')
        return tmp