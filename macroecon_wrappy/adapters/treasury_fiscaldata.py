#!/usr/bin/env python3
"""
treasury fiscal data Adapter 

Notes:
* ref: https://fiscaldata.treasury.gov/datasets/
* ~~simple AdapterInterface cache is used~~
* full dataset table extracted 
  - from here: https://fiscaldata.treasury.gov/api-documentation/
  - maintained here: 'macroecon_wrappy/macroecon_wrappy/adapters/data/
  


TODO:
* move to Extractor (do not use the earlier api wrapper)
* create endpoint with params
* complicated response does not allow for simple conversion to Metric
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .adapter import AdapterInterface
from ..metric import Metric

import pandas as pd
from bs4 import BeautifulSoup

from pathlib import Path
import requests


class TreasuryFiscalAdapter(AdapterInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper()        #treasury_client = FederalTreasuryClient()
        self.wrapper_name = 'treasury_fiscaldata'
        self._set_cache_path(auth, self.wrapper_name)

        #config
        dataset_table_files = [
            'macroecon_wrappy/adapters/data/API Documentation _ U.S. Treasury Fiscal Data - 1.html',
            'macroecon_wrappy/adapters/data/API Documentation _ U.S. Treasury Fiscal Data - 2.html'
        ]
        self.datasets = []
        for file in dataset_table_files:
            filepath = Path() / file
            with open(filepath, 'r') as f:
                html = f.read()
            soup = BeautifulSoup(html)
            tbl = soup.find('table', {'aria-describedby': 'list-of-endpoints-id'})
            ths = tbl.findAll('thead')[0].findAll('th')
            trs = tbl.findAll('tbody')[0].findAll('tr')
            for tr in trs:
                tds = tr.findAll('td')
                dataset = {
                    f'{ths[0].text}-name': tds[0].find('a').text, 
                    f'{ths[0].text}-href': tds[0].find('a').get('href'),
                    ths[1].text: tds[1].text,
                    ths[2].text: tds[2].text,
                    ths[3].text: tds[3].text
                }
                self.datasets.append(dataset)

    def get_data(self, seriesId):
        """Get data from API and return object of class Metric.
        
        seriesId == 'other_data-historical_debt_outstanding'
        """
        ds = pd.DataFrame(self.datasets)

        k,v = seriesId.split('-')
        if k not in ds['Dataset-name'].to_list(): raise Exception(f'key {k} not in mapping')
        if v not in ds['Table Name'].to_list(): raise Exception(f'value {v} not in mapping')
        tbl_name = ds[ds['Table Name']==v]
        
        #TODO:stopped here



        #check if already available
        pd_series = self._get_data_if_cached(key=seriesId)
        if pd_series:
            return pd_series
        
        #o/w get data
        key_group = getattr(self.wrapper, k)
        value_method_to_call = getattr(key_group(), v)
        result_dict = value_method_to_call(page_number=2000, page_size=1000)    #TODO:this may not be a param for all methods
        if not result_dict:
            raise Exception(f'no data found for seriesId {seriesId}')
        """
        pd_df = pd.DataFrame(result_dict['data'])
        pd_df['record_date'] = pd.to_datetime(pd_df['record_date'])
        pd_series = pd_df.set_index('record_date')['debt_outstanding_amt']
        series_meta_dict = result_dict['meta']

        #TODO: metadata mapping needs
        metric = Metric(pd_series)
        metric.title = pd_series.name
        metric.id = None
        metric.source = None
        metric.references = None
        metric.notes = None
        metric.date_range = pd_series.index.min(), pd_series.index.max(), 
        metric.frequency = None
        metric.last_updated = pd_series.index.max()
        metric.obseravation_date = None
        metric.release = None
        metric.seasonal_adjustment = None
        metric.seasonal_adjustment_short = None
        metric.t = pd_series.index.max() - pd_series.index.min()
        metric.units = None
        metric.units_short = None
        metric.set_metadata(**series_meta_dict)

        #cache and return results
        self._cache_data(seriesId, metric)
        return metric
        """
        return result_dict
    '''
    def get_metadata(self, seriesId):
        """Get the seriesId metadata.
        If it is not already extracted, request it, or add to it
        with another request if current metadata does not have it.
        """
        if self._metadata_df.shape[0] == 0:
            metadata_df = self.wrapper.search(seriesId)
            self._metadata_df =  metadata_df 
        subset = self._metadata_df[self._metadata_df.id==seriesId]
        if subset.shape[0] == 1:
            series_meta_dict = subset.iloc[0].to_dict()
            return series_meta_dict
        else:
            metadata_df = self.wrapper.search(seriesId)
            new_metadata_df = pd.concat([self._metadata_df, metadata_df], axis=0).drop_duplicates()
            self._metadata_df = new_metadata_df
        subset = self._metadata_df[self._metadata_df.id==seriesId]
        #TODO: is this necessary???
        if subset.shape[0] == 1:
            series_meta_dict = subset.iloc[0].to_dict()
            return series_meta_dict
        else:
            return None'
    '''