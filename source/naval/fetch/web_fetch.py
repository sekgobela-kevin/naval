from io import FileIO
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse
import requests

from pdfminer.high_level import extract_text
import os, sys, io
import tempfile

from ..fetch.fetch_base import Fetch_Base

class Web_Fetch(Fetch_Base):
    '''Crawls the web for data'''

    def __init__(self, url, content_type=None, *args, **kwargs):
        super().__init__(url, content_type=None, *args, **kwargs)
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    @classmethod
    def source_to_text(cls, source) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        return source

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid'''
        if not isinstance(source, str):
            raise TypeError(f"source should be string not ", type(source))
        try:
            parsed = urlparse(source )
            return all([parsed.scheme, parsed.netloc])
        except:
            return False

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if source is active'''
        if not isinstance(source, str):
            raise TypeError(f"source should be string not ", type(source))
        # you can perfor validation based on returned code mostly 200
        try:
            return urlopen(source).getcode() == 200
        except urllib.error.URLError:
            pass
        return False

    @classmethod
    def get_filename_from_url(cls, url):
        '''Create filename from url'''
        if not isinstance(url, str):
            raise TypeError(f"url should be string not ", type(url))
        parsed = urlparse(url)
        filename = f"{parsed.scheme}_{parsed.netloc}_{parsed.path}"
        filename = filename.replace("/", "_")
        # add .html to filename if no path part to url
        # its likely to be webpage which is mostly HTML
        if not parsed.path:
            filename += ".html"
        return filename

    def fetch_to_disc(self, source: str) -> str:
        '''Read raw data from source and save to file'''
        if not isinstance(source, str):
            raise TypeError(f"source should be string not ", type(source))
        request = requests.get(self._source, headers=self.headers, stream=True)
        for chunk in request.iter_content(chunk_size=128):
            self.file.write(chunk)
        self.file.seek(0)
        return self.file


if __name__ == "__main__":
    url = 'http://docs.python.org/library/tempfile.html'
    crawl_obj = Web_Fetch(url=url)

    for i in range(10):
        print(len(crawl_obj.request().read()))

