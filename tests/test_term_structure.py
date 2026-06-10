#!/usr/bin/env python3
"""
test TermStructure class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ == "MIT"

#wrappy
from macroecon_wrappy.auth import Auth
from macroecon_wrappy.extractors import (
    TreasuryExtract,
    FrbnyExtract
)
from macroecon_wrappy.extractors.frbny import FrbnyClient
from macroecon_wrappy.metric import Metric
from macroecon_wrappy.measure import Measure
from macroecon_wrappy.epoch import Epoch
from macroecon_wrappy.term_structure import TermStructure
from macroecon_wrappy.utils import delete_folder
from tests.data.test_data import (
    df_series,
    df_cycle,

    df_mmmffa,
    df_tb1yr
)
metric1 = Metric(df_series['value1'])
metric2 = Metric(df_series['value2'])
epoch = Epoch(df_cycle)

#external
import pandas as pd

#stdlib
from pathlib import Path
from datetime import date



#setup
secrets_path = Path('SECRETS.yaml')
cache_path = Path('./tests/tmp')
auth = Auth(secrets_path, cache_path)
auth.load_secrets()



def test_term_structure_from_metrics():
    wd = cache_path / 'treasury'
    delete_folder(wd)
    #load contrived data
    ts = TermStructure(metrics=[metric1, metric2], cycle_epoch=epoch)
    assert ts.get_data_timeframe() == {'from':'', 'to': ''}
    assert type(ts.get_yields()) == Measure
    assert type(ts.get_yield_curve(date='')) == Measure

def test_term_structure_from_metrics():
    wd = cache_path / 'treasury'
    delete_folder(wd)
    TreasuryExtract.set_config(auth)
    ts_treas = TermStructure(TreasuryExtract, epoch)
    #load nominal treasury yields
    assert True == True