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
    FiscalExtract,
    OfrExtract,
    FrbnyExtract
)
from macroecon_wrappy.extractors.treasury_fiscaldata import TreasuryFiscalClient
from macroecon_wrappy.extractors.treasury_ofr import TreasuryOfrClient
from macroecon_wrappy.extractors.frbny import FrbnyClient

from macroecon_wrappy.metric import Metric
from macroecon_wrappy.epoch import Epoch
from macroecon_wrappy.utils import delete_folder

#external
import pandas as pd

#stdlib
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
    assert recessions.df().shape == (35,3)
    results = []
    for idx, col in enumerate(['start', 'end']):
        result = recessions.df().columns[idx] == col
        results.append(result)
    assert all(results)
    recessions_from_cache = NberExtract.get_data(name)
    assert recessions_from_cache.df().shape == (35,3)

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

def test_treasury_fiscaldata():
    wd = cache_path / 'treasury_fiscaldata'
    delete_folder(wd)
    FiscalExtract.set_wrapper(auth, TreasuryFiscalClient)
    raw_dict = FiscalExtract.get_raw('Historical Debt Outstanding')
    assert isinstance(raw_dict, dict)
    assert list(raw_dict.keys()) == ['data','meta','links']
    assert len(raw_dict['data']) >= 0
    raw_dict = FiscalExtract.get_raw('Detail of Treasury Securities Outstanding')
    assert isinstance(raw_dict, dict)
    assert len(raw_dict['data']) >= 0

def test_treasury_ofr():
    wd = cache_path / 'treasury_ofr'
    delete_folder(wd)
    OfrExtract.set_wrapper(auth, TreasuryOfrClient)
    check_dataset_series_are_populated = OfrExtract.datasets_with_series.values()
    assert len(check_dataset_series_are_populated) == 5
    metric_NYPD_PD_AFtD_AG_A = OfrExtract.get_data(seriesIds=['NYPD-PD_AFtD_AG-A'])[0]
    assert isinstance(metric_NYPD_PD_AFtD_AG_A, Metric)

def test_frbny():
    '''
    wd = cache_path / 'frbny'
    delete_folder(wd)
    FrbnyExtract.set_wrapper(auth, FrbnyClient)
    check_dataset_series_are_populated = FrbnyExtract.datasets_with_series.values()
    assert len(check_dataset_series_are_populated) == 5
    metric_NYPD_PD_AFtD_AG_A = FrbnyExtract.get_data(seriesIds=['NYPD-PD_AFtD_AG-A'])[0]
    assert isinstance(metric_NYPD_PD_AFtD_AG_A, Metric)'
    '''
    assert True == True