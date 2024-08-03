#!/usr/bin/env python3
"""
internetarchive Adapter

referneces:
* internet archive (Adapter)
  - explanation of sources: https://stackoverflow.com/questions/33811582/how-to-access-wayback-machine-programmatically
  - internet archive: https://archive.org/developers/internetarchive/quickstart.html
  - wayback machine: https://github.com/jsvine/waybackpack
* useful market feed urls:
  - bloomberg: https://web.archive.org/web/20080526075131mp_/http://www.bloomberg.com/news/economy/
  - cnbc: https://web.archive.org/web/20000302145140/http://www.cnbc.com/market/markets_main.asp
  - wsj: https://web.archive.org/web/20041016054515/http://online.wsj.com/public/us
  - routers: https://web.archive.org/web/20000621104155/http://www.reuters.com/news/default.asp?b=rcom:world_news
  - nytimes: https://web.archive.org/web/20100101173218/http://www.nytimes.com/
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .adapter import AdapterInterface
from ..metric import Metric

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
random.seed(1)


def get_text_from_html(file_or_str):
    """Get text from html file or url link.

    ref: https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    """
    if file_or_str.is_file():
        file = file_or_str
        with open(file, 'r') as f:
            html = f.read()
    else:
        url = file_or_str
        html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    paragraphs = '\n'.join(chunk for chunk in chunks if chunk)
    text = paragraphs.replace('\n',' ')
    return text




class InternetArchiveAdapter(AdapterInterface):
    """Interface for wrapper adapter
    
    Usage::
    >>> InternetArchiveExtract.set_wrapper(auth, waybackpack)
    >>> config = {
        'urls':["http://www.dol.gov/"], 
        'models':[]
        }
    >>> event = InternetArchiveExtract.get_data(config)
    """

    def set_wrapper(self, auth, wrapper):
        """Set the authenticated wrapper."""
        self.wrapper = wrapper
        self.wrapper_name = 'internet_archive'
        self._set_cache_path(auth, self.wrapper_name)

    def get_data(self, config):
        """Get data from API and return object of class Metric."""
        # TODO: fix cache abilities
        urls_model_results = {}
        for url in config['urls']:
            #check if already available
            model_results = self._get_data_if_cached(key=url)
            if model_results:
                urls_model_results[url] = model_results
                continue
            #o/w get data
            snapshots = self.wrapper.search(url=url, 
                                            to_date=config['end'], 
                                            from_date=config['start']
                                            )
            timestamps = [snap["timestamp"] for snap in snapshots]
            sampled_ts = random.sample(timestamps, config['sample'])
            pack = self.wrapper.Pack(url, sampled_ts)
            dirpath = self.cache_path
            pack.download_to(dirpath, no_clobber=True)
            '''
            #example of individual asset extraction
            first = self.wrapper.Asset(url, timestamps[0])
            session = self.wrapper.Session(follow_redirects=True)
            content = first.fetch(session=session)
            '''
            #run models
            model_results = {}
            html_files = list(self.cache_path.rglob('*.html'))
            for file in html_files:
                date = int(''.join(filter(str.isdigit, file.__str__())))
                content = get_text_from_html(file)
                tmp_results = []
                for model in config['models']:
                    results = model(content)
                    tmp_results.extend(results)
                model_results[date] = tmp_results
            urls_model_results[url] = model_results

            #cache and return results
            #TODO: self._cache_data(url, model_results)
        return urls_model_results