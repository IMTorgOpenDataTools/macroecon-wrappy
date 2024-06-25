#!/usr/bin/env python3
"""
fredapi Adapter 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .adapter import AdapterInterface
from ..metric import Metric


class FredApiAdapter(AdapterInterface):
    """Interface for wrapper adapter"""
    def set_wrapper(self, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper
    
    def get_data(self, seriesId):
        """Get data from API and return object of class Metric."""
        data = self.wrapper.get_series = seriesId
        metadata_df = self.wrapper.search(seriesId)
        metric = Metric(data)
        row_dict = metadata_df.iloc[0].to_dict()
        metric.set_metadata(**row_dict)
        return metric
