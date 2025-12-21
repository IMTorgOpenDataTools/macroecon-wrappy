#!/usr/bin/env python3
"""
simple utility functions
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import pandas as pd

from pathlib import Path
import os, shutil



def delete_folder(dir):
    """Delete folder and all child dirs, files."""
    dir_path = Path(dir)
    if dir_path.is_dir():
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        shutil.rmtree(dir_path)


def separate_batch_call_to_dict_of_dfs(batch_tickers):
    """
    Docstring for separate_batch_call_to_dict_of_dfs
    
    :param batch_tickers: Description
    Usage::
        dfs = separate_batch_call_to_dict_of_dfs(top_ten)
    """
    top_lvls = list( set( batch_tickers.columns.get_level_values(0)) )
    symbols = list( set( batch_tickers.columns.get_level_values(1)) )
    dfs = {}
    for symbol in symbols:
        df = pd.DataFrame()
        for idx, lvl in enumerate(top_lvls):
            tmp = batch_tickers.loc[:, (lvl, symbol)]
            df.insert(idx, lvl, tmp)
        dfs[symbol] = df
    return dfs


def get_recursive_items(data, criteria_func=None):
    """
    TODO: use this at ref
    Recursively finds items where criteria_func(key, value) is True.
    Returns a list of (key, value) tuples.

    integrate with yahoo.py

    Usage: 
        #get all items where the value is an integer > 100
        my_data = {"a": 50, "b": {"c": 150, "d": [200, {"e": 300}]}}
        found = get_recursive_items(my_data, lambda k, v: isinstance(v, int) and v > 100)
        # Output: [('c', 150), ('e', 300)]
    """
    def criteria_func(k,v):
        v in [float, int, str, dict]
        return True
    
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            # Check if the current key-value pair meets criteria
            if criteria_func(k, v):
                results.append((k, v))
            
            # Recurse if value is a nested dict or list
            if isinstance(v, (dict, list)):
                results.extend(get_recursive_items(v, criteria_func))
                
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                results.extend(get_recursive_items(item, criteria_func))
                
    return results

