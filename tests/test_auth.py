#!/usr/bin/env python3
"""
Tests for Auth
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from macroecon_wrappy.auth import Auth

from pathlib import Path
import os




def test_auth():
    secrets_path = Path('tests/data/test-SECRETS.yaml')
    cache_path = Path('tests/tmp/')
    auth = Auth(secrets_path, cache_path)
    auth.load_secrets()
    assert 'fred_api_key' in auth.data.keys()
    assert 'fred_api_key' in os.environ
    assert auth.obb.user.credentials.fred_api_key == os.environ['fred_api_key']
    assert auth.data['fred_api_key'] == '<add-key-here>'
    assert auth.cache_path == Path('tests/tmp')
    assert auth.get_cache_sources().__len__() >= 0