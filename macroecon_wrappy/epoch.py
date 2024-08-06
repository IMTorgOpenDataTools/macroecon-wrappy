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


def yearsago(years, from_date=None):
    """Years ago from some date."""
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year-years)


def time_diff(begin, end=None, units='months', pretty=True):
    """Number of years between two dates.
    ref: https://stackoverflow.com/questions/765797/convert-timedelta-to-years
    """
    if end is None:
        end = datetime.now()
    result = None
    num_years = (end - begin).days / 365.2425
    if units == 'months':
        num_months = num_years * 12
        result = num_months
    elif units=='years':
        num_years = int(num_years)
        if begin > yearsago(num_years, end):
            result = num_years - 1
        else:
            result = num_years
    return round(result, 2)



class TimePeriod:
    """..."""

    def __init__(self, item):
        self.value = item
        for k,v in item.to_dict().items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        return str(self.value)


class Event(TimePeriod):
    """..."""
    pass


class Span(TimePeriod):
    """..."""
    pass


def epoch_row_factory(row):
    """Factor for creating Span or Event from Epoch row."""
    diff = (row[Epoch._names[1]] - row[Epoch._names[0]]).total_seconds()
    if diff <= Epoch._determine_event_duration_cutoff_seconds:
        return Event(row)
    else:
        dt = f'{row.start.year}/{row.start.month}/{row.start.day} - {row.end.year}/{row.end.month}/{row.end.day}'
        diff_months = time_diff(row.start, row.end)
        span = Span(row)
        span.name = f'{diff_months} mo | {dt}'
        return span
    



class Epoch:
    """..."""
    _names = ['start', 'end', 'name']
    _span_duration_seconds = 0
    _determine_event_duration_cutoff_seconds = 0

    def __init__(self, df_or_list):
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
            for idx, col in enumerate(df.columns[:len(self._names[:2])].tolist()):
                colname = self._names[idx]
                df.rename(columns={ col: colname }, inplace = True)
                df[colname] = pd.to_datetime(df[colname])
            df[self._names[2]] = ''
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
            row = df[ (df[colnames[0]] < dt) & (df[colnames[1]] > dt) ].iloc[0]
        elif isinstance(idx_or_date, str):
            try:
                dt_str = idx_or_date
                dt = datetime.strptime(dt_str, '%Y-%m-%d')
            except Exception as e:
                print(f'arg {dt_str} is of type `str` but cannot be converted to datetime')
                print(e)
            colnames = self._names
            df = self.df()
            row = df[ (df[colnames[0]] < dt) & (df[colnames[1]] > dt) ].iloc[0]
        item_event_or_span = epoch_row_factory(row)
        return item_event_or_span
    
    def get_items(self):
        """Generator to get each item (Event / Span) from the Epoch."""
        rows = self.df().shape[0]
        for row_idx in range(rows):
            item_event_or_span = self.idx(row_idx)
            yield item_event_or_span

    def to_long(self):
        """Convert data to long-format DataFrame"""
        cols = self._names
        tmp = self.df(dates_only=True)
        tmp['date'] = tmp.index
        tmp.reset_index(drop=True, inplace=True)
        tmp = pd.melt(tmp, id_vars='date', value_vars=cols, var_name='grp', value_name='value')
        return tmp