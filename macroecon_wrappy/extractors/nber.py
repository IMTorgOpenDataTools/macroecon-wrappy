#!/usr/bin/env python3
"""
nber Extractor

data index:
* https://www.nber.org/research/data?page=1&perPage=50
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .extractor import ExtractorInterface
from ..epoch import Epoch
#from ..span import Span

import requests
import pandas as pd


class NberExtractor(ExtractorInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_config(self, auth):
        """Set the authenticated wrapper."""
        self.urls = {
            'recessions': 'https://data.nber.org/data/cycles/business_cycle_dates.json'
        }
        self.wrapper_name = 'nber'
        self.cache_path = None
        self.cache_file = None
        self._set_cache_path(auth, self.wrapper_name)
    
    def get_raw(self, name):
        """Get raw data from API in json format."""
        #check if already available
        raw = self._get_data_if_cached(key=name)
        if raw:
            return raw
        #o/w make request
        url = self.urls[name]
        data = requests.get(url)
        json = data.json()
        #cache and return results
        self._cache_data(name, json)
        return json
    
    def get_data(self, name):
        """Get data from API and return object of class Epoch."""
        json = self.get_raw(name)
        epoch = Epoch(json)
        return epoch