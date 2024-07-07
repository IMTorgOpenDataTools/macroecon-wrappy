#!/usr/bin/env python3
"""
Extractor interface to integrate webpages for scraping.

Only a small number of Extractors are provided. 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


class ExtractorInterface():
    """Interface for url extractor"""
    def set_config(self):
        """Set the configuration elements."""
        raise NotImplementedError("Implement this for APi-wrapper")
    
    def get_data(self, *args, **kwargs):
        """Get data from URL and return object of different classes."""
        raise NotImplementedError("Implement this for APi-wrapper")