#!/usr/bin/env python3
"""
Authentication integrated with external dependencies
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import yaml
from pathlib import Path
import os


class Auth:
    """Load and maintain env variables from a YAML file.
    
    Also, maintain module configuration data.
    """
    def __init__(self, secrets, cache=None):
        self.secrets_path = None
        self.data = None
        self.cache_path = None
        test_secrets = Path(secrets)
        if test_secrets.is_file() and test_secrets.suffix in ['.yml','.yaml']:
            self.secrets_path = test_secrets
        else:
            raise TypeError
        if cache:
            test_cache = Path(cache)
            if not test_cache.is_dir():
                test_cache.mkdir(parents=True, exist_ok=False)
                print(f'cache created: {test_cache.resolve()}')
            self.cache_path = test_cache

    def __repr__(self) -> str:
        pass
    
    def load_secrets(self):
        """Load secrets file."""
        with open(self.secrets_path, 'r') as fh:
            data = yaml.safe_load(fh)
        self.data = {k:v for (k,v) in data.items()}
        return True
    
    def get_cache_sources(self):
        """Get the sources (directories) within cache directory."""
        if self.cache_path:
            subfolders = [ f.path for f in os.scandir(self.cache_path) if f.is_dir() ]
            return subfolders
        else:
            raise Exception('no cache_path directory is set')