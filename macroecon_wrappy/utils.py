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






def criteria_func(key, value):
    return type(value) in [str, int, float]

def filter_nested_dict(data, criteria_func):
    """
    Recursively filters items in a nested dictionary based on a criteria function.

    Args:
        data (dict): The input nested dictionary.
        criteria_func (function): A function that takes a key and a value,
                                  and returns True if the item should be kept.

    Returns:
        dict: A new dictionary containing only the filtered items.
    
    Usage:
        tmp1 = filter_nested_dict(tkr.__dict__, criteria_func)
    """
    filtered_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            # Recursively filter nested dictionaries
            nested_result = filter_nested_dict(value, criteria_func)
            # Only add the key if the nested result is not empty
            if nested_result:
                filtered_data[key] = nested_result
        elif criteria_func(key, value):
            # Apply the criteria function for non-dict items
            filtered_data[key] = value
    return filtered_data






import json

def serialize_dir(obj):
    """
    Ingests an object and returns a JSON-serializable dict of its dir() attributes.
    """
    serializable_dict = {}
    for attr_name in dir(obj):
        if '_' not in attr_name:
            try:
                value = getattr(obj, attr_name)
                #attempt to JSON encode to verify serializability
                json.dumps(value)
                serializable_dict[attr_name] = value
            except (TypeError, OverflowError, AttributeError):
                #fallback for non-serializable types (functions, classes, etc.)
                serializable_dict[attr_name] = str(value)
    return serializable_dict




#TODO:the below is not used but may be useful for more in-depth attempt at object conversion to json
import json
import inspect

def serialize_object_to_dict(obj, seen_objects=None):
    """
    Recursively serializes an object's attributes (from dir(obj)) into a JSON-compatible nested dictionary.

    Args:
        obj: The object to serialize.
        seen_objects: A set to track objects already visited to prevent recursion loops.

    Returns:
        A JSON-compatible dictionary or a simple value representation.
    """
    if seen_objects is None:
        seen_objects = set()

    #handle primitive types that are directly JSON serializable
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    #handle common iterable types (lists, tuples, sets)
    if isinstance(obj, (list, tuple, set)):
        return [serialize_object_to_dict(item, seen_objects) for item in obj]
    #check for recursion
    if id(obj) in seen_objects:
        return None#f"<Recursive reference to {type(obj).__name__}>"
    seen_objects.add(id(obj))
    #for other objects, iterate through attributes using dir()
    if isinstance(obj, object):
        data_dict = {}
        #use dir() to get all attributes, including those dynamically added
        for attr_name in dir(obj):
            #filter out built-in/magic methods and non-public attributes
            if attr_name.startswith('__') and attr_name.endswith('__'):
                continue
            try:
                attr_value = getattr(obj, attr_name)
                #filter out methods and functions
                if inspect.ismethod(attr_value) or inspect.isfunction(attr_value) or inspect.isbuiltin(attr_value):
                    continue
                #recursively serialize the attribute's value
                data_dict[attr_name] = serialize_object_to_dict(attr_value, seen_objects)
            except Exception:
                #handle cases where getattr fails (e.g., restricted access)
                data_dict[attr_name] = None#f"<Could not serialize {type(attr_value).__name__}>"
        return data_dict

    # For types not explicitly handled (e.g., complex objects not using standard attributes), 
    # return a string representation.
    return None    #str(obj)


def object_to_json_nested_dict(obj):
    """
    Converts a Python object into a JSON serializable nested dictionary.
    """
    nested_dict = serialize_object_to_dict(obj)
    try:
        json.dumps(nested_dict)
    except TypeError as e:
        print(f"Warning: Resulting dictionary is not fully JSON serializable: {e}")
    return nested_dict