#!/usr/bin/env python3
"""
Frbny Extractor

Notes:
* includes the following data:
  - API [ref](https://markets.newyorkfed.org/static/docs/markets-api.html)
  - dashboard [ref](https://www.newyorkfed.org/markets/data-hub)
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .extractor import ExtractorInterface
from ..metric import Metric

import pandas as pd
from bs4 import BeautifulSoup

from pathlib import Path
import requests


class FrbnyExtractor(ExtractorInterface):
    """..."""

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper()        #treasury_client = FederalTreasuryClient()
        self.wrapper_name = 'treasury_ofr'
        self._set_cache_path(auth, self.wrapper_name)

    def get_raw(self, *args, **kwargs):
        """Get data from URL and return in raw fromat.
        
        #TODO:put bulk of request handling, here.
        """
        raise NotImplementedError("Implement this for API-wrapper")
    
    def get_data(self, *args, **kwargs):
        """Get data from URL and return object of internal classes.
        
        #TODO:use `.get_raw()` to get unstructured response
        #TODO:change to `.get_metric()` and return that object
        """
        raise NotImplementedError("Implement this for API-wrapper")
    




import json
import requests
import pathlib

from typing import Dict
from datetime import datetime
from datetime import date

#import logging
class Logging():
    def __init__(self):
        pass
    def info(self, txt):
        print(txt)
    def error(self, msg):
        print(msg)
logging = Logging()


class FrbnyClient():
    """..."""

    def __init__(self) -> None:
        """Initializes the `FederalTreasuryClient`.

        ### Usage
        ----
            >>> treasury_client = FederalTreasuryClient()
        """
        self.resource = 'https://data.financialresearch.gov/'
        self.version = 'v1/'

    def __repr__(self) -> str:
        """String representation of the `TreasuryOfrSession` object.
        str_representation = '<FederalTreasuryClient.TreasuryOfrSession (active=True, connected=True)>'
        return str_representation"""
        raise NotImplementedError("Implement this for API-wrapper")

    def build_url(self, endpoint: str) -> str:
        """..."""
        raise NotImplementedError("Implement this for API-wrapper")
    
    def make_request(
        self,
        method: str,
        endpoint: str,
        start_date: str,
        end_date: str,
        periodicity: str,
        
        #params: dict = None,
        #data: dict = None,
        #json_payload: dict = None
    ) -> Dict:
        raise NotImplementedError("Implement this for API-wrapper")