#!/usr/bin/env python3
"""
Extractor interface to integrate webpages for scraping.

Only a small number of Extractors are provided. 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pickle


class ExtractorInterface():
    """Interface for url extractor"""
    def set_config(self, auth):
        """Set the configuration elements."""
        self.urls = {'name': 'url'}
        self.wrapper_name = None
        self.cache_path = None
        self.cache_file = None
        self._set_cache_path(auth, self.wrapper_name)
        raise NotImplementedError("Implement this for API-wrapper")
    
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
        """Save data to cache.
        
        #TODO:use dict to add metadata | data_dict = {key:seriesId, 'data': df, 'metadata':metadata}
          - must determine the types: Metric, df, metadata, etc.
        """
        with open(self.cache_file, 'rb') as f:
            pkl_dict = pickle.load(f)
        pkl_dict[key] = data
        with open(self.cache_file, 'wb') as f:
            pickle.dump(pkl_dict, f)
        return True

    def _get_data_if_cached(self, key):
        """Check if data is cached and retrieve if so.

        #TODO:update for the above change
        """
        with open(self.cache_file, 'rb') as f:
            pkl_dict = pickle.load(f)
        if key in pkl_dict.keys():
            return pkl_dict[key]
        else:
            return None