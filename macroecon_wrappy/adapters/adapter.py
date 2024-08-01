#!/usr/bin/env python3
"""
Adapter interface to integrate API-wrappers with Metric class.

Only a small number of adapters are provided for select API-wrappers. 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import pickle

class AdapterInterface():
    """Interface for wrapper adapter"""

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = None
        self.wrapper_name = None
        self.cache_path = None
        self.cache_file = None
        raise NotImplementedError("Implement this for APi-wrapper")
    
    def get_data(self, *args, **kwargs):
        """Get data from API and return object of class Metric."""
        raise NotImplementedError("Implement this for APi-wrapper")
    

    def _set_cache_path(self, auth, name):
        """Set the directory (and file) to use as cache."""
        cache_path = auth.cache_path / name
        cache_path.mkdir(parents=False, exist_ok=True)
        self.cache_path = cache_path
        self.cache_file = self.cache_path / f'{name}.pickle'
        with open(self.cache_file, 'wb') as f:
            pickle.dump({}, f)
        return True

    def _cache_data(self, key, data):
        """Save data to cache."""
        with open(self.cache_file, 'rb') as f:
            pkl_dict = pickle.load(f)
        pkl_dict[key] = data
        with open(self.cache_file, 'wb') as f:
            pickle.dump(pkl_dict, f)
        return True

    def _get_data_if_cached(self, key):
        """Check if data is cached and retrieve if so."""
        with open(self.cache_file, 'rb') as f:
            pkl_dict = pickle.load(f)
        if key in pkl_dict.keys():
            return pkl_dict[key]
        else:
            return None