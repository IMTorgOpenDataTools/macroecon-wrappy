#!/usr/bin/env python3
"""
treasury Extractor

data index:
* https://www.nber.org/research/data?page=1&perPage=50
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .extractor import ExtractorInterface
#from ..span import Span

import requests
import pandas as pd

import re


class UsTreasuryExtractor(ExtractorInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_config(self):
        """Set the authenticated wrapper."""
        self.urls = {
            'coupon-2000': {'url':'https://home.treasury.gov/system/files/276/Website-PDO-4-A-Coupons-Jan-2000-Sep%202009.xls',
                            'cols': ['issue date', 'security type', 'security term', 'coupon rate or spread', 'cusip', 'maturity date', 'total issue', 'federal reserve banks', 'depository institutions', 'individuals', 'dealers and brokers', 'pension and retirement funds and ins. co.', 'investment funds', 'foreign and international', 'other']},
            'coupon-2009': {'url':'https://home.treasury.gov/system/files/276/June-25-2024-IC-Coupons.xls',
                            'cols': ['issue date', 'security type', 'coupon rate or spread', 'cusip', 'maturity date', 'total issue', 'federal reserve banks', 'depository institutions', 'individuals', 'dealers and brokers', 'pension and retirement funds and ins. co.', 'investment funds', 'foreign and international', 'other']},
            'bill-2000': {'url':'https://home.treasury.gov/system/files/276/Website-IC-allotments-Bills-Aug-2001-Sep-2009.xls',
                          'cols': ['issue date', 'security term', 'auction high rate %', 'cusip', 'maturity date', 'total issue', 'federal reserve banks', 'depository institutions', 'individuals', 'dealers and brokers', 'pension and retirement funds and ins. co.', 'investment funds', 'foreign and international', 'other']},
            'bill-2009': {'url':'https://home.treasury.gov/system/files/276/June-7-2024-IC-Bills.xls',
                          'cols': ['issue date', 'security term', 'auction high rate %', 'cusip', 'maturity date', 'total issue', 'federal reserve banks', 'depository institutions', 'individuals', 'dealers and brokers', 'pension and retirement funds and ins. co.', 'investment funds', 'foreign and international', 'other']}
        }
    
    def get_data(self, name):
        """Get data from API and return object of class Metric."""
        keys = list(self.urls.keys())
        tgt_keys = [key for key in keys if key.split('-')[0] == name]
        results = pd.DataFrame()
        for key in tgt_keys:
            item = self.urls[key]
            try:
                df = pd.read_excel(item['url'], skiprows=3, names=item['cols'])
            except Exception as e:
                print(e)
            results = pd.concat([df, results], ignore_index=True, axis=0)
            results.dropna(subset=['issue date'], inplace=True)
        return results