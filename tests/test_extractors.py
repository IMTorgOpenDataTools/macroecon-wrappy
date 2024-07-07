#!/usr/bin/env python3
"""
test Extractor class and url extractor instances
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#wrappy
from macroecon_wrappy.extractors import (
    NberExtract
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
    for idx, col in enumerate(['peak','trough']):
        result = recessions.df().columns[idx] == col
        results.append(result)
    assert all(results)