#!/usr/bin/env python3
"""
FRED Endpoints
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import requests
from bs4 import BeautifulSoup
import lxml



url_popular_series='https://fred.stlouisfed.org/tags/series?ob=pv'

def get_most_popular_series(n):
    """Get the 'n' most-popular series from the web app"""
    url=url_popular_series
    mx_page = (n // 15) + 1
    page_nums = range(0,mx_page)
    print(f'scraping {mx_page} pages')
    
    results = []
    for pg in page_nums:
        if pg>1:
            suffix = f'&t=&et=&pageID={pg}'
            endpt = url + suffix
        else:
            endpt = url
        try:
            raw = requests.get(endpt)
            txt = raw.text
            html = BeautifulSoup(txt, features="xml")
            tbl = html.body.find('table', attrs={'id':'series-pager'})
            if not tbl:
                continue
            hdrs = tbl.findAll('h3')
            for hdr in hdrs:
                a = hdr.find('a')
                if not a:
                    continue
                href = a.get('href')
                series = href.split('/series/')[1]
                name = a.getText()
                results.append({
                    'Series ID': series,
                    'Name': name
                })
        except Exception as e:
            print(f'There was a problem with: endpt {endpt} ')
            print(e)
            pass
    print(f'populated {len(results)} series')
    return results[:n]