#!/usr/bin/env python3
"""
Make available all implemented values. 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#import all adapters
from .fredapi import FredApiAdapter
from .yahoo import YahooAdapter



#make available
FredApi = FredApiAdapter()
YahooFin = YahooAdapter()