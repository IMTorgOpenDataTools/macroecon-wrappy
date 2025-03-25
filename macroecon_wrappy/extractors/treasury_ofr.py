#!/usr/bin/env python3
"""
treasury ofr Extractor

Notes:
* includes the following data:
  - short-term funding monitor, [ref](https://www.financialresearch.gov/short-term-funding-monitor/api/)
  - hedge funds monitor
  - um money market fund monitor
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .extractor import ExtractorInterface
from ..metric import Metric

import pandas as pd
from bs4 import BeautifulSoup

from pathlib import Path
import requests


class TreasuryOfrExtractor(ExtractorInterface):
    """..."""

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper()        #treasury_client = FederalTreasuryClient()
        self.wrapper_name = 'treasury_ofr'
        self._set_cache_path(auth, self.wrapper_name)

        #config datasets and endpoints
        self.suffixes = {
            'all_series_in_dataset':'metadata/mnemonics',   #all series of a dataset
            'seriesIds': 'series/multifull'     #download multiple time series; default to most inclusive range
        }
        #TODO: this can be requested with: https://data.financialresearch.gov/v1/series/dataset
        self.datasets_with_series = {
            'mmf': None,	#OFR U.S. Money Market Fund Data Release
            'repo': None,	#OFR U.S. Repo Markets Data Release
            'fnyr': None,	#Federal Reserve Bank of New York Reference Rates
            'nypd': None,	#Federal Reserve Bank of New York Primary Dealer Statistics
            'tyld' : None   #Treasury Constant Maturity Rates
        }
        self._get_dataset_metadata()

    def _get_dataset_metadata(self):
        """Populate dataset metadata"""
        for key in self.datasets_with_series.keys():
            pd_df = self._get_data_if_cached(key)
            if not pd_df:
                jsonl = self.wrapper.make_request(
                    method='get',
                    endpoint=self.suffixes['all_series_in_dataset'] + '?dataset=' + key,
                    start_date=None,
                    end_date=None,
                    periodicity=None
                    )
                if jsonl:
                    pd_df = pd.DataFrame(jsonl)
            self._cache_data(key, pd_df)
            self.datasets_with_series[key] = pd_df
        return True

    def _get_all_series(self):
        """Get all available datasets' series."""
        df_series = pd.DataFrame({
            'mnemonic': [], 
            'series_name': [], 
            'dataset': []
            })
        for ds, ds_series in self.datasets_with_series.items():
            ds_series['dataset'] = ds
            df_series = pd.concat([df_series, ds_series])
        return df_series

    def _check_series_exists(self, seriesIds=[]):
        """..."""
        result = {}
        for ts in seriesIds:
            if ts in self._get_all_series()['mnemonic'].to_list():
                result[ts] = True
            else:
                result[ts] = False
        return result

    def get_data(self, seriesIds=[], start_date=None, end_date=None, periodicity=None):
        """Get data from URL and return object of different classes.
        
        #TODO:use the .get_raw() and xform to return Metric
        """
        #check seriesId is available
        checks = self._check_series_exists(seriesIds)
        if not all(checks.values()):
            print(f'ERROR: the following series are not availble:')
            for series, check in checks.items():
                if check == False:
                    print(f'* {series}')
        #make request and populate response as metric
        all_series = self._get_all_series()
        metrics = []
        for seriesId in seriesIds:
            pd_df = self._get_data_if_cached(seriesId)
            if not pd_df:
                #TODO:&start_date=2018-04-01&end_date=2019-04-01&periodicity=Q
                json = self.wrapper.make_request(
                    method='get',
                    endpoint=self.suffixes['seriesIds'] + '?mnemonics=' + seriesId,
                    start_date=None,
                    end_date=None,
                    periodicity=None
                    )
                if json:
                    pd_df = pd.DataFrame(data=json[seriesId]['timeseries']['aggregation'], columns=['timestamp', seriesId ])
                    pd_df['timestamp'] = pd.to_datetime(pd_df['timestamp'])
                    pd_df.set_index(keys='timestamp', inplace=True)
                    pd_series = pd_df[seriesId]
                    metadata = json[seriesId]['metadata']
                    #self._cache_data(seriesId, pd_df)    #TODO:use dict to add metadata | data_dict = {'data': df, 'metadata':metadata}
            metric = Metric(pd_series)
            metric.title = metadata['release']['short_name']
            metric.id = metadata['mnemonic']
            metric.source = None
            metric.references = None
            metric.description = all_series[all_series.mnemonic==seriesId]['series_name'].values[0]
            metric.notes = metadata['description']['notes']
            metric.date_range = metadata['schedule']['start_date'], metadata['schedule']['last_update'], 
            metric.frequency = metadata['schedule']['observation_frequency']
            metric.last_updated = metadata['schedule']['last_update']
            metric.obseravation_date = None
            metric.release = metadata['release']
            metric.seasonal_adjustment = None
            metric.seasonal_adjustment_short = None
            metric.t = pd_series.index.max() - pd_series.index.min()
            metric.units = metadata['unit']
            metric.units_short = None
            metric.set_metadata(**metadata)

            #cache and return results
            self._cache_data(seriesId, metric)
            metrics.append(metric)
        return metrics



import json
import requests
import pathlib

from typing import Dict
from datetime import datetime
from datetime import date

#import logging
class Logging():
    def __init__(self):
        pass
    def info(self, txt):
        print(txt)
    def error(self, msg):
        print(msg)
logging = Logging()


class TreasuryOfrClient():
    """..."""

    def __init__(self) -> None:
        """Initializes the `FederalTreasuryClient`.

        ### Usage
        ----
            >>> treasury_client = FederalTreasuryClient()
        """
        self.resource = 'https://data.financialresearch.gov/'
        self.version = 'v1/'

    def __repr__(self) -> str:
        """String representation of the `TreasuryOfrSession` object."""
        str_representation = '<FederalTreasuryClient.TreasuryOfrSession (active=True, connected=True)>'
        return str_representation

    def build_url(self, endpoint: str) -> str:
        """Builds the full url for the endpoint.

        ### Parameters
        ----
        endpoint : str
            The endpoint being requested.

        ### Returns
        ----
        str:
            The full URL with the endpoint needed.
        """
        url = self.resource + self.version + endpoint
        return url

    def make_request(
        self,
        method: str,
        endpoint: str,
        start_date: str,
        end_date: str,
        periodicity: str,
        
        #params: dict = None,
        #data: dict = None,
        #json_payload: dict = None
    ) -> Dict:
        """Handles all the requests in the library.

        ### Overview:
        ---
        A central function used to handle all the requests made in the library,
        this function handles building the URL, defining Content-Type, passing
        through payloads, and handling any errors that may arise during the request.

        ### Parameters:
        ----
        method : str
            The Request method, can be one of the
            following: ['get','post','put','delete','patch']

        endpoint : str
            The API URL endpoint.

        ...



        ### Returns:
        ----
            A Dictionary object containing the JSON values.
        """

        # Build the URL.
        url = self.build_url(endpoint=endpoint)
        logging.info(txt="URL: {url}".format(url=url) )
        '''
        if type(params)==dict:
            if 'realtime_start' in params and isinstance(params['realtime_start'], datetime):
                params['realtime_start'] = params['realtime_start'].date().isoformat()

            if 'realtime_end' in params and isinstance(params['realtime_end'], datetime):
                params['realtime_end'] = params['realtime_end'].date().isoformat()

            if 'tag_names' in params and isinstance(params['tag_names'], list):
                logging.info('Joining Tag Names: {lst}'.format(
                    lst=params['tag_names']))
                params['tag_names'] = ';'.join(params['tag_names'])

            if 'exclude_tag_names' in params and isinstance(params['exclude_tag_names'], list):
                logging.info('Joining Exclude Tag Names: {lst}'.format(
                    lst=params['exclude_tag_names']))
                params['exclude_tag_names'] = ';'.join(params['exclude_tag_names'])
        else:
            params = {}
        '''
        params = {}
        data = {}
        json_payload = {}

        params_cleaned = params.copy()
        params_cleaned['api_key'] = 'xxxxxxxx'

        logging.info(
            "PARAMS: {params}".format(params=params_cleaned)
        )

        # Define a new session.
        request_session = requests.Session()
        request_session.verify = True

        # Define a new request.
        request_request = requests.Request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json_payload
        ).prepare()

        # Send the request.
        response: requests.Response = request_session.send(
            request=request_request
        )

        # Close the session.
        request_session.close()

        # If it's okay and no details.
        if response.ok and len(response.content) > 0:
            return response.json()

        elif len(response.content) > 0 and response.ok:
            return {
                'message': 'response successful',
                'status_code': response.status_code
            }

        elif not response.ok:

            # Define the error dict.
            error_dict = {
                'error_code': response.status_code,
                'response_url': response.url,
                'response_body': json.loads(response.content.decode('ascii')),
                'response_request': dict(response.request.headers),
                'response_method': response.request.method,
            }

            # Log the error.
            logging.error(
                msg=json.dumps(obj=error_dict, indent=4)
            )

            raise requests.HTTPError()