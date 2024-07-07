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
#from ..span import Span

import requests
import pandas as pd


class NberExtractor(ExtractorInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_config(self):
        """Set the authenticated wrapper."""
        self.urls = {
            'recessions': 'https://data.nber.org/data/cycles/business_cycle_dates.json'
        }
    
    def get_data(self, name):
        """Get data from API and return object of class Metric."""
        url = self.urls[name]
        data = requests.get(url)
        return data.json()