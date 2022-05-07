from ..fetch.fetch_base import Fetch_Base

import tempfile
import os, sys, io
import random

class File_Fetch(Fetch_Base):
    '''Provide methods for fetching data from file'''
    def __init__(self, source, *args, **kwargs):
        '''source - file object or path to file\n
        *args- optional arguments to pass to file.open()\n
        **kwagrs - optional arguments to pass to file.open()\n
        '''
        super().__init__(source)

    @staticmethod
    def open(source: str or io.FileIO, *args, **kwargs) -> io.FileIO:
        '''Opens file and return file object\n
        source - file object or path to file\n
        *args- optional arguments to pass to file.open()\n
        **kwagrs - optional arguments to pass to file.open()\n'''
        if not isinstance(source, (str, io.FileIO)):
            TypeError("source: should be file obj or string not ", type(source))
        if isinstance(source, str):
            return open(source,*args, **kwargs)
        # then source arg refers to file object
        return source
    
    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid'''
        if not isinstance(source, (str, io.FileIO)):
            TypeError("file should be file obj or string not ", type(source))
        if File_Fetch.is_source_unknown(source):
            # source was autotiatially created
            # it does not have a source
            return True
        return os.path.isfile(source)

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if data in source is accessible'''
        return File_Fetch.is_source_valid(source)


if __name__ == "__main__":

    string = tempfile.TemporaryFile()
    string.write(b"jhhh")
    print(os.path.isfile(__file__))
    crawl_obj = File_Fetch(string)
    print(len(crawl_obj))
    #print(crawl_obj[0].get_text())
    print(crawl_obj.is_source_active(crawl_obj.get_source()))
    print(crawl_obj.request())
