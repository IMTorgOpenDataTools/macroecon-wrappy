#!/usr/bin/env python3
"""
treasury fiscal data Adapter 

Note:
* simple AdapterInterface cache is used
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .adapter import AdapterInterface
from ..metric import Metric

import pandas as pd


class TreasuryFiscalAdapter(AdapterInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper()        #treasury_client = FederalTreasuryClient()
        self.wrapper_name = 'treasury_fiscaldata'
        self._set_cache_path(auth, self.wrapper_name)

    def get_data(self, seriesId):
        """Get data from API and return object of class Metric.
        
        seriesId == 'other_data-historical_debt_outstanding'
        """
        #config
        mapping = {
            'other_data': ['average_interest_rates', 'balance_sheets', 'gold_reserve', 'historical_debt_outstanding', 'interest_expense']
        }
        k,v = seriesId.split('-')
        if k not in mapping.keys(): raise Exception(f'key {k} not in mapping')
        if v not in mapping[k]: raise Exception(f'value {v} not in mapping')
        
        #check if already available
        pd_series = self._get_data_if_cached(key=seriesId)
        if pd_series:
            return pd_series
        
        #o/w get data
        key_group = getattr(self.wrapper, k)
        value_method_to_call = getattr(key_group(), v)
        result_dict = value_method_to_call(page_size=1000)    #TODO:this may not be a param for all methods
        if not result_dict:
            raise Exception(f'no data found for seriesId {seriesId}')
        pd_df = pd.DataFrame(result_dict['data'])
        pd_df['record_date'] = pd.to_datetime(pd_df['record_date'])
        pd_series = pd_df.set_index('record_date')['debt_outstanding_amt']
        series_meta_dict = result_dict['meta']

        #TODO: metadata mapping needs
        metric = Metric(pd_series)
        metric.title = pd_series.name
        metric.id = None
        metric.source = None
        metric.references = None
        metric.notes = None
        metric.date_range = pd_series.index.min(), pd_series.index.max(), 
        metric.frequency = None
        metric.last_updated = pd_series.index.max()
        metric.obseravation_date = None
        metric.release = None
        metric.seasonal_adjustment = None
        metric.seasonal_adjustment_short = None
        metric.t = pd_series.index.max() - pd_series.index.min()
        metric.units = None
        metric.units_short = None
        metric.set_metadata(**series_meta_dict)

        #cache and return results
        self._cache_data(seriesId, metric)
        return metric
    
    def get_metadata(self, seriesId):
        """Get the seriesId metadata.
        If it is not already extracted, request it, or add to it
        with another request if current metadata does not have it.
        """
        if self._metadata_df.shape[0] == 0:
            metadata_df = self.wrapper.search(seriesId)
            self._metadata_df =  metadata_df 
        subset = self._metadata_df[self._metadata_df.id==seriesId]
        if subset.shape[0] == 1:
            series_meta_dict = subset.iloc[0].to_dict()
            return series_meta_dict
        else:
            metadata_df = self.wrapper.search(seriesId)
            new_metadata_df = pd.concat([self._metadata_df, metadata_df], axis=0).drop_duplicates()
            self._metadata_df = new_metadata_df
        subset = self._metadata_df[self._metadata_df.id==seriesId]
        #TODO: is this necessary???
        if subset.shape[0] == 1:
            series_meta_dict = subset.iloc[0].to_dict()
            return series_meta_dict
        else:
            return None