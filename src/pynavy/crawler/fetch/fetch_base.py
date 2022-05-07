import os, sys, io
import time

class Fetch_Base():
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
        self._source = filename

    def get_source(self) -> str:
        return self._source

    def get_file(self):
        '''Returns file object kept by this object'''
        return self.file

    def is_empty(self):
        '''Checks if underlying file object is empty'''
        self.file.seek(0, 2)
        return self.file.tell() == 0

    @staticmethod
    def open(source: str or io.IOBase, *args, **kwargs) -> io.IOBase:
        '''Opens file and return file object\n
        source - file object or path to file\n
        *args- optional arguments to pass to file.open()\n
        **kwagrs - optional arguments to pass to file.open()\n'''
        if not isinstance(source, (str, io.IOBase)):
            raise TypeError("source: should be file obj or string not ", 
            type(source))
        if isinstance(source, str):
            if os.path.isfile(source):
                return open(source,*args, **kwargs)
            else:
                raise ValueError(f"source({source}) does not refer to file",
                "Overide this method if source is not meant to point to file")
        # then source arg refers to file object
        return source

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid'''
        raise NotImplementedError()

    @staticmethod
    def is_source_active(source: str) -> bool:
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
        if not isinstance(source, str):
            TypeError("source should be string not ", type(source))
        return Fetch_Base.unknown_source_prefix in source

    @staticmethod
    def get_filename(source: io.IOBase or str):
        '''Creates filename from path or file object\n
        source - file object or path to file'''
        if not isinstance(source, (str, io.IOBase)):
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
        raise NotImplementedError()

    def request(self, *args, **kwarg) -> io.IOBase:
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