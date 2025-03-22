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
    secrets_path = Path('tests/data/test-SECRETS.yaml')
    cache_path = Path('tests/tmp/')
    auth = Auth(secrets_path, cache_path)
    auth.load_secrets()
    assert 'API_KEY_FED' in auth.data.keys()
    assert auth.data['API_KEY_FED'] == '<add-key-here>'
    assert auth.cache_path == Path('tests/tmp')
    assert auth.get_cache_sources().__len__() >= 0