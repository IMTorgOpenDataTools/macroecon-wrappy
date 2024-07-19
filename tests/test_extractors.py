#!/usr/bin/env python3
"""
test Extractor class and url extractor instances
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#wrappy
from macroecon_wrappy.extractors import (
    NberExtract,
    TreasuryExtract
)
#from macroecon_wrappy.metric import Metric
from macroecon_wrappy.epoch import Epoch


#sys
from pathlib import Path


def test_nber():
    name = 'recessions'
    NberExtract.set_config()
    data = NberExtract.get_data(name)
    recessions = Epoch(data)
    assert recessions.df().shape == (35,2)
    results = []
    for idx, col in enumerate(['start', 'end']):
        result = recessions.df().columns[idx] == col
        results.append(result)
    assert all(results)

def test_treasury():
    names = ['coupon', 'bill']
    TreasuryExtract.set_config()
    coupons_df = TreasuryExtract.get_data(names[0])
    bills_df = TreasuryExtract.get_data(names[1])
    assert coupons_df.shape == (1803, 15)
    assert bills_df.shape == (4867, 14)