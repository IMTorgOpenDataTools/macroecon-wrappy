#!/usr/bin/env python3
"""
Load data from sources
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from .RM_sources.nber import url_recession_bars
from .RM_sources import fred

import pandas as pd
import requests



def get_most_popular_series(n, src='fred'):
    """Get the 'n' most-popular series from the web app"""
    results = None
    match src:
        case 'fred':
            results = fred.get_most_popular_series(n=n)
        case _:
            raise Exception(f'must choose from one of the `src` options')

    return results


def get_recession_bars():
    """Get timespans needed to graph recession bars."""
    url = url_recession_bars
    raw = requests.get(url)
    df = pd.DataFrame(raw.json())
    df['peak'] = pd.to_datetime(df['peak'])
    df['trough'] = pd.to_datetime(df['trough'])
    return df