#!/usr/bin/env python3
"""
treasury fiscal data Adapter 

Notes:
* ref: https://fiscaldata.treasury.gov/datasets/
* this code is adapted from repo: https://github.com/areed1192/us-federal-treasury-python-api
* full dataset table extracted 
  - from here: https://fiscaldata.treasury.gov/api-documentation/
  - maintained here: 'macroecon_wrappy/macroecon_wrappy/adapters/data/
* ~~simple AdapterInterface cache is used~~
  


TODO:
* ~~move to Extractor (do not use the earlier api wrapper)~~
* create endpoint with params
* ~~complicated response does not allow for simple conversion to Metric
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


class TreasuryFiscalExtractor(ExtractorInterface):
    """Interface for wrapper adapter"""

    _metadata_df = pd.DataFrame()

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper()        #treasury_client = FederalTreasuryClient()
        self.wrapper_name = 'treasury_fiscaldata'
        self._set_cache_path(auth, self.wrapper_name)

        #config datasets
        dataset_table_files = [
            'macroecon_wrappy/extractors/data/API Documentation _ U.S. Treasury Fiscal Data - 1.html',
            'macroecon_wrappy/extractors/data/API Documentation _ U.S. Treasury Fiscal Data - 2.html'
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

    def get_raw(self, seriesId):
        """Get data from API and return object of class pd.DataFrame.
        
        seriesId: corresponds with df['Table Name'] which has unique values
        """
        ds = pd.DataFrame(self.datasets)
        if seriesId not in ds['Table Name'].to_list(): 
            raise Exception(f'value {seriesId} not in mapping')
        tbl = ds[ds['Table Name'] == seriesId]
        
        #check if already available
        pd_df = self._get_data_if_cached(key=seriesId)
        if pd_df:
            return pd_df
        
        #o/w get data
        docs = tbl['Dataset-href'].values[0]
        endpoint = tbl.Endpoint.values[0]
        #self.wrapper.build_url(endpoint)
        data = self.wrapper.make_request(
            method = 'get',
            endpoint = endpoint, 
            params = None,
            data = None,
            json_payload = None
        )
        return data

    def get_data(self, *args, **kwargs):
        """Get data from URL and return object of different classes."""
        raise NotImplementedError("Implement this for API-wrapper")







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
logging = Logging()


class FederalTreasuryClient():

    def __init__(self) -> None:
        """Initializes the `FederalTreasuryClient`.

        ### Usage
        ----
            >>> treasury_client = FederalTreasuryClient()
        """
        self.resource = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service'

        '''
        if not pathlib.Path('logs').exists():
            pathlib.Path('logs').mkdir()
            pathlib.Path('logs/fred_api_log.log').touch()
        logging.basicConfig(
            filename="logs/treasury_api_log.log",
            level=logging.INFO,
            encoding="utf-8",
            format=log_format
        )'''

    def __repr__(self) -> str:
        """String representation of the `TreasurySession` object."""

        # define the string representation
        str_representation = '<FederalTreasuryClient.TreasurySession (active=True, connected=True)>'

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

        url = self.resource + endpoint

        return url

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        json_payload: dict = None
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

        params : dict (optional, Default=None) 
            The URL params for the request.

        data : dict (optional, Default=None)
            A data payload for a request.

        json : dict (optional, Default=None)
            A json data payload for a request

        ### Returns:
        ----
            A Dictionary object containing the JSON values.
        """

        # Build the URL.
        url = self.build_url(endpoint=endpoint)
        logging.info(txt="URL: {url}".format(url=url) )

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