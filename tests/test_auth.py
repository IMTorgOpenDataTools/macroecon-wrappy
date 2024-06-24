#!/usr/bin/env python3
"""
Tests for Auth
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.auth import Auth

from pathlib import Path




def test_auth():
    filepath = Path('tests/data/test-SECRETS.yaml')
    auth = Auth(filepath)
    auth.load()
    assert 'API_KEY_FED' in auth.data.keys()
    assert auth.data['API_KEY_FED'] == '<add-key-here>'