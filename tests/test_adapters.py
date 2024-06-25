#!/usr/bin/env python3
"""
test Adapter class and API-wrapper instances
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.auth import Auth
from macroecon_wrappy.adapters import (
    FredApi
)
from macroecon_wrappy.metric import Metric

from fredapi import Fred

from pathlib import Path



def test_fredapi():
    filepath = Path('SECRETS.yaml')     # <<< must use actual api key
    auth = Auth(filepath)
    auth.load()
    fred = Fred(api_key=auth.data['API_KEY_FED'])

    FredApi.set_wrapper(fred)
    metric = FredApi.get_data('GDP')
    assert type(metric) == Metric