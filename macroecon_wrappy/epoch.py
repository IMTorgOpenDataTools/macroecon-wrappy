#!/usr/bin/env python3
"""
Epoch class that combines multiple Span items.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#from .span import Span

import pandas as pd


class Epoch:
    """..."""

    def __init__(self, df):
        self.df_data = pd.DataFrame(df)

    def df(self):
        """..."""
        return self.df_data