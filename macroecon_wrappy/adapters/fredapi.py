#!/usr/bin/env python3
"""
fredapi Adapter 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .adapter import AdapterInterface
from ..metric import Metric

import pandas as pd


class FredApiAdapter(AdapterInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_wrapper(self, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper
    
    def get_data(self, seriesId):
        """Get data from API and return object of class Metric."""
        pd_series = self.wrapper.get_series(seriesId)
        series_meta_dict = self.get_metadata(seriesId)
        if not series_meta_dict:
            raise Exception(f'no metadata found for seriesId {seriesId}')
        metric = Metric(pd_series)
        metric.set_metadata(**series_meta_dict)
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
        if subset.shape[0] == 1:
            series_meta_dict = subset.iloc[0].to_dict()
            return series_meta_dict
        else:
            return None


        



