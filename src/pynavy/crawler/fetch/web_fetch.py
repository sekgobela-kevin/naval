from io import FileIO
from urllib.request import urlopen
from urllib.parse import urlparse
import requests

from pdfminer.high_level import extract_text
import os, sys, io
import tempfile

from ..fetch.fetch_base import Fetch_Base

class Web_Fetch(Fetch_Base):
    '''Crawls the web for data'''

    def __init__(self, url, *args, **kwarg):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.file = self.open(*args, **kwarg)
        # create object as if its a file
        super().__init__(self.file)
        # set source as the orginal url instead of using file object
        self._source = url

    @staticmethod
    def open(*args, **kwargs) -> io.IOBase:
        '''Opens temporary file\n
        *args- optional arguments to pass to TemporaryFile()\n
        **kwagrs - optional arguments to pass to TemporaryFile()\n'''
        # then source arg refers to file object
        return tempfile.TemporaryFile()

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid'''
        try:
            parsed = urlparse(source)
            return all([parsed.scheme, parsed.netloc])
        except:
            return False

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if source is active'''
        # you can perfor validation based on returned code mostly 200
        return urlopen(source).getcode() == 200

    @staticmethod
    def get_filename_from_url(url):
        '''Create filename from url'''
        parsed = urlparse(url)
        filename = f"{parsed.scheme}_{parsed.netloc}_{parsed.path}"
        return filename.replace("/", "_")

    def fetch_to_disc(self, source: str) -> str:
        '''Read raw data from source and save to file'''
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

