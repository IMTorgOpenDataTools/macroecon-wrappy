#!/usr/bin/env python3
"""
simple utility functions
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


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