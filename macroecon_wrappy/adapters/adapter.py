#!/usr/bin/env python3
"""
Adapter interface to integrate API-wrappers with Metric class.

Only a small number of adapters are provided for select API-wrappers. 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


class AdapterInterface():
    """Interface for wrapper adapter"""
    def set_wrapper(self, wrapper):
        """Set the authenticated wrapper."""
        raise NotImplementedError("Implement this for APi-wrapper")
    
    def get_data(self, *args, **kwargs):
        """Get data from API and return object of class Metric."""
        raise NotImplementedError("Implement this for APi-wrapper")