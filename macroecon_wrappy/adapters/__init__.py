#!/usr/bin/env python3
"""
Make avialable all implemented values. 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#import all adapters
from .fredapi import FredApiAdapter



#make available
FredApi = FredApiAdapter()