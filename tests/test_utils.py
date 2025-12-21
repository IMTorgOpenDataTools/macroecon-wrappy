#!/usr/bin/env python3
"""
test Adapter class and API-wrapper instances
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy import utils

import json


def test_remove_non_serializable():
    broken_data = {
        "name": "Alice",
        "age": 30,
        "hobbies": ["reading", "cycling"],
        "callback": lambda x: x,  # Not serializable
        "data_set": {1, 2, 3},    # Set is not JSON serializable
        "nested":{
            "callback": lambda x: x,  # Not serializable
        }
    }
    corrected_data = '{"name": "Alice", "age": 30, "hobbies": ["reading", "cycling"], "callback": null, "data_set": null, "nested": {"callback": null}}'
    json_str = json.dumps(broken_data, default=utils.replace_non_serializable)
    assert json_str  == corrected_data