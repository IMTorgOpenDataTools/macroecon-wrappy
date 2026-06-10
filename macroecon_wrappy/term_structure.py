#!/usr/bin/env python3
"""
TermStructure class that combines multiple interest rate Measure items.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .extractors.extractor import ExtractorInterface
from .metric import Metric
from .measure import Measure
from .epoch import Epoch

import pandas as pd
import numpy as np

from copy import deepcopy


class TermStructure(Measure):
    """"Debt securities of 'similar' credit quality and their relationship
    between market interest rates (yields) and the remaining time to maturity.

    Notes:
        Financial economists generally use three primary theories to explain why the term structure changes shape:
        * Expectations Theory: assumes that long-term rates reflect what investors expect short-term rates to be in the future
        * Liquidity Preference Theory: suggests that investor inherently prefer short-term, highly liquid assets and must be paid a 'term premium' to take on the higher price volatility of long-term bonds.
        * Makret Segmentation Theory: assumes that different investors (like short-term money market funds vs. long-term pension funds) operate in isolated maturity sectors, meaning supply and demand within each specific bucket independently dictate the rates.
    
    Usage:
        ```
        yield metrics = [bills, notes, bonds]
        ts = TermStructure(key='yield', metric_or_metric_list=yield_metrics)
        ts.get_yield_curve()
        #or
        TreasuryExtract.set_config(auth)
        ts_treas = TermStructure(extractors=[TreasuryExtract], cycle_epoch=epoch)
        check_current = ts_treas.load_data()
    """
    def __init__(self, extractors=None, metrics=None, cycle_epoch=None):
        self.available_keys = ['yields', 'rates']
        self.extractors = None
        if (extractors and metrics) or (not (extractors and metrics)):
            raise Exception('must use either argument `extractors` (to source data) or `metrics` (to provide data) - not both')
        if extractors:
            if type(extractors) == list:
                try:
                    for extractor in extractors:
                        assert type(extractor) == ExtractorInterface
                except:
                    raise Exception(f'argument `extractors` mst be of type List with {ExtractorInterface} items')
                self.extractors = extractors
            else:
                raise Exception(f'argument `extractors` mst be of type List with {ExtractorInterface} items')
        elif metrics:
            self._check_metrics(metrics)
            super().__init__(metrics, cycle_epoch)
            #?  setattr(self, key) = self.df()
        else:
            super().__init__()
            if cycle_epoch:
                self.set_cycle(cycle_epoch)
    
    def _check_metrics(self, metrics):
        if type(metrics) == list:
            for metric in metrics:
                try: 
                    assert type(metric) == Metric
                except:
                    raise Exception(f'argument `metrics` must be of List with type {Metric} items')
                try:
                    assert metric.type in self.available_keys
                except:
                    raise Exception(f'arg `key` must be one of the available_keys: {self.available_keys}')
        else:
            raise Exception(f'argument `metrics` must be of List with type {Metric} items')
        
    def load_data(self, from_date='', to_date=''):
        for extractor in self.extractors:
            metrics = extractor.get_data()
            self._check_metrics(metrics)
            self.add_metric(metric_or_metric_list=metrics)

    def get_yields(self):
        return self.df()
    
    def get_yield_curve(self, from_date, to_date=None):
        measure_subset = self.subset_by_time(from_date, to_date)
        return measure_subset
    
    def get_AUC(self, date=''):
        maturities = self.df().columns
        auc_values = self.df().apply(lambda row: np.trapzoid(row[maturities], maturities), axis=1)
        auc_df = auc_values.reset_index(name='auc')
        return auc_df
    
    def get_ema_diffs(self, time_unit='daily'):
        emas = []
        for metric in self.get_metric():
            ema = metric.ema(span=20, adjust=False)
            emas.append(ema)
        return emas
    
    def term_premium(self, date='', type=''):
        pass

    def get_policy_interference(self, from_date='', to_date=''):
        #TODO: AUC short-end - AUC long-end
        pass

    def get_duration(self, date='', type=''):
        pass