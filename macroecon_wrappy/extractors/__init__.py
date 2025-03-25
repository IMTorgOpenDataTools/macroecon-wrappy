#!/usr/bin/env python3
"""
Make available all implemented values. 
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

#import all extractors
from .nber import NberExtractor
from .treasury import UsTreasuryExtractor
from .treasury_fiscaldata import TreasuryFiscalExtractor
from .treasury_ofr import TreasuryOfrExtractor
from .frbny import FrbnyExtractor


#make available
NberExtract = NberExtractor()
TreasuryExtract = UsTreasuryExtractor()
FiscalExtract = TreasuryFiscalExtractor()
OfrExtract = TreasuryOfrExtractor()
FrbnyExtract = FrbnyExtractor()