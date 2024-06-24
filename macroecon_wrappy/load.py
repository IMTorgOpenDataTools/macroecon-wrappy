#!/usr/bin/env python3
"""
Load data from sources
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from .sources import fred



def get_most_popular_series(n, src='fred'):
    """Get the 'n' most-popular series from the web app"""
    results = None
    match src:
        case 'fred':
            results = fred.get_most_popular_series(n=n)
        case _:
            raise Exception(f'must choose from one of the `src` options')

    return results