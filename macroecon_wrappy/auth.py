#!/usr/bin/env python3
"""
Authentication integrated with external dependencies
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import yaml
from pathlib import Path


class Auth:
    """Load and maintain env variables from a YAML file."""
    def __init__(self, filepath):
        testpath = Path(filepath)
        if testpath.is_file() and testpath.suffix in ['.yml','.yaml']:
            self.filepath = testpath
            self.data = None
        else:
            raise TypeError
        
    def load(self):
        with open(self.filepath, 'r') as fh:
            data = yaml.safe_load(fh)
        self.data = {k:v for (k,v) in data.items()}
        return True