#!/usr/bin/env python3
"""
test Extractor class and url extractor instances
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#wrappy
from macroecon_wrappy.auth import Auth
from macroecon_wrappy.extractors import (
    NberExtract,
    TreasuryExtract,
)
#from macroecon_wrappy.metric import Metric
from macroecon_wrappy.epoch import Epoch
from macroecon_wrappy.utils import delete_folder

#sys
from pathlib import Path


#setup
secrets_path = Path('SECRETS.yaml')     # <<< must use actual api key
cache_path = Path('./tests/tmp')
auth = Auth(secrets_path, cache_path)
auth.load_secrets()



def test_nber():
    wd = cache_path / 'nber'
    delete_folder(wd)
    NberExtract.set_config(auth)
    name = 'recessions'
    recessions = NberExtract.get_data(name)
    assert recessions.df().shape == (35,2)
    results = []
    for idx, col in enumerate(['start', 'end']):
        result = recessions.df().columns[idx] == col
        results.append(result)
    assert all(results)
    recessions_from_cache = NberExtract.get_data(name)
    assert recessions_from_cache.df().shape == (35,2)

def test_treasury():
    wd = cache_path / 'treasury'
    delete_folder(wd)
    names = ['coupon', 'bill']
    TreasuryExtract.set_config(auth)
    coupons_df = TreasuryExtract.get_raw(names[0])
    bills_df = TreasuryExtract.get_raw(names[1])
    assert coupons_df.shape == (1803, 15)
    assert bills_df.shape == (4867, 14)
    TreasuryExtract.set_config(auth)
    coupons_df_from_cache = TreasuryExtract.get_raw(names[0])
    assert coupons_df_from_cache.shape == (1803, 15)