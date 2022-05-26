from io import FileIO
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
import requests, mimetypes
import logging


from pdfminer.high_level import extract_text
import os, sys, io
import tempfile

from ..fetch.fetch_base import Fetch_Base
from ..utility import directories


class Web_Fetch(Fetch_Base):
    '''Crawls the web for data'''
    headers = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, url, content_type=None, *args, **kwargs):
        super().__init__(url, content_type=None, *args, **kwargs)

    @classmethod
    def source_to_text(cls, source) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        return source

    @classmethod
    def source_to_content_type(cls, source):
        '''Return content type of source(url, filepath, etc)\n
        source - url, filepath, file object, etc\n'''
        if not mimetypes.inited: mimetypes.init()
        source_text = cls.source_to_text(source)
        # handle url without extension(likey pointing to html)
        # e.g http://example.com/tutorials
        path_part = urlparse(source_text).path
        if path_part:
            # check if path part has extension
            if not directories.get_file_extension(path_part):
                source_text += " .html"
        else:
            # no path part mean not extension
            source_text += " .html"
        return mimetypes.guess_type(source_text)[0]

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

    @classmethod
    def is_source_active(cls, source: str) -> bool:
        '''Checks if source is active'''
        if not isinstance(source, str):
            raise TypeError(f"source should be string not ", type(source))
        req = urllib.request.Request(source)
        for key, val in cls.headers.items():
            req.add_header(key, val)
        # you can perfor validation based on returned code mostly 200
        try:
            code = urlopen(req).getcode()
            return  code == 200
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

    @classmethod
    def fetch_to_file(cls, source: str, file: io.FileIO, timeout=60,
    conn_timeout=5, chunk_size=2**13, max_retries=2, verify=True) -> str:
        '''Fetch data from source to file and return file object\n
        source - file path or file like object\n
        file - file like object to store data\n
        timeout - timeout for fetching data\n
        conn_timeout - timeout for connecting to server(connection timeout)'''
        if not isinstance(source, str):
            raise TypeError(f"source should be string not ", type(source))
        # create session with max retries for url
        session = requests.Session()
        session.mount(source, HTTPAdapter(max_retries))
        # perform request
        response = requests.get(source, headers=cls.headers, stream=True,
        timeout=(conn_timeout,timeout), verify=verify)
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
        return file


if __name__ == "__main__":
    url = 'https://example.com'
    crawl_obj = Web_Fetch(url=url)
    print(crawl_obj.is_source_active(url))
    crawl_obj.request()
    print(crawl_obj.read())
