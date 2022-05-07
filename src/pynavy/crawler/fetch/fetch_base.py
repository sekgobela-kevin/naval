from ..text.text import Text
import os, sys, io
import time

class Fetch_Base(Text):
    '''Base class for fetching raw data from source(url, path, etc).
    Data from source is stored in file after fetched from its source.'''
    '''Class for representing text broken into sections'''
    unknown_prefix = "__unknown"
    # added to source if source is unknown
    unknown_source_prefix = f"{unknown_prefix}_source"
    # added to source if source is unknown
    unknown_tile_prefix = f"{unknown_prefix}_title"

    def __init__(self, source, *args, **kwargs):
        '''source - file object or path to file\n
        *args- optional arguments to pass to file.open()\n
        **kwagrs - optional arguments to pass to file.open()\n
        '''
        self.file = self.open(source, *args, **kwargs)
        filename = self.get_filename(self.file)
        super().__init__(filename)

    def get_file(self):
        return self.file

    def is_empty(self):
        '''Checks if underlying file object is empty'''
        self.file.seek(0, 2)
        return self.file.tell() == 0

    @staticmethod
    def open(source: str or io.FileIO, *args, **kwargs) -> io.FileIO:
        '''Opens file and return file object\n
        source - file object or path to file\n
        *args- optional arguments to pass to file.open()\n
        **kwagrs - optional arguments to pass to file.open()\n'''
        return NotImplementedError()

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid'''
        raise NotImplementedError()

    @staticmethod
    def is_source_active(self, source: str) -> bool:
        '''Checks if data in source is accessible'''
        raise NotImplementedError()

    @staticmethod
    def get_unknown_source(*args):
        '''Creates random source in case source is not known'''
        right_part = ""
        for arg in args:
            right_part += arg
        return f"{Fetch_Base.unknown_source_prefix}_{right_part}_{time.time()}"

    @staticmethod
    def is_source_unknown(source: str):
        '''Checks if source was auto generated'''
        return Fetch_Base.unknown_source_prefix in source

    @staticmethod
    def get_filename(source: io.FileIO or str):
        '''Creates filename from path or file object\n
        source - file object or path to file'''
        if not isinstance(source, (str, io.FileIO)):
            TypeError("source should be file obj or string not ", type(source))
        if isinstance(source, str): 
            return source
        elif "name" in dir(source):
            if isinstance(source.name, (str)):
                return source.name
        return Fetch_Base.get_unknown_source()


    def fetch(self, *args, **kwagrs) -> str:
        '''Reads data located at file\n
        *args- optional arguments to pass to file.read()\n
        **kwagrs - optional arguments to pass to file.read()\n'''
        self.file.seek(0)
        return self.file.read(*args, **kwagrs)

    def fetch_to_disc(self, source: str) -> str:
        '''Fetch data from source to file and return file object'''
        # no need to fetch data is already in file
        return self.file

    def request(self, *args, **kwarg) -> io.FileIO:
        '''Read data from file path and return file object'''
        # check if file is closed or empty
        if self.file.closed:
            # open new file if closed
            self.file = self.open(self._source, *args, **kwarg)
        elif self.is_empty():
            # write to file if empty
            self.fetch_to_disc(self._source)
        self.file.seek(0)
        return self.file


    def close(self):
        '''Closes file opened by the object'''
        self.file.close()