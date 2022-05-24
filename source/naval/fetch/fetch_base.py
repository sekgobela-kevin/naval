import mimetypes
import os, sys, io
import time
import tempfile
import shutil

class Fetch_Base():
    '''Base class for fetching raw data from source(url, path, etc).
    Data from source is stored in file after fetched from its source.'''
    '''Class for representing text broken into sections'''
    unknown_prefix = "__unknown"
    # added to source if source is unknown
    unknown_source_prefix = f"{unknown_prefix}_source"
    # added to source if source is unknown
    unknown_tile_prefix = f"{unknown_prefix}_title"

    def __init__(self, source, content_type=None, *args, **kwargs):
        '''source - url, filepath, file object, etc\n
        content_type - content type of fetch object data.
        Could be in form e.g 'text/', '.html', 'html', 'text/plain' or '
        file.txt. If None, content type is guessed from source.\n
        *args- optional arguments to pass to file.open()\n
        **kwagrs - optional arguments to pass to file.open()\n
        '''
        self._source = source
        self._source_text = self.source_to_text(source)
        assert isinstance(self._source_text, str), self._source_text
        self.content_type = self.guess_type(source, content_type)
        # files should always be opened in binary mode
        self.file = self.open(source, *args, **kwargs)

    def get_source(self) -> str or io.IOBase:
        '''Returns source(file path, file obj, url, etc)'''
        return self._source

    @classmethod
    def source_to_text(cls, source) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        if isinstance(source, str):
            return source
        return cls.get_unknown_source()

    def get_source_text(self) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        return self._source_text

    def get_content_type(self):
        '''Returns content type of fetched data'''
        return self.content_type

    @classmethod
    def source_to_content_type(cls, source):
        '''Return content type of source(url, filepath, etc)\n
        source - url, filepath, file object, etc\n'''
        if not mimetypes.inited: mimetypes.init()
        source_text = cls.source_to_text(source)
        if not isinstance(source_text, str):
            raise Exception("source_to_text() should return str or None", 
            type(source_text))
        if not source_text:
            return None
        return mimetypes.guess_type(source_text)[0]

    @classmethod
    def transform_content_type(cls, content_type):
        '''Transforms argument content type\n
        content_type - string in form e.g 'text/', '.html', 
        'html', 'text/plain' or 'file.txt'''
        if not (isinstance(content_type, str) or content_type == None):
            raise TypeError("content_type should be string or None", 
            type(content_type))
        if content_type == "" or content_type == None:
            return None
        elif content_type[-1] == "/":
            # applies to e.g text/
            return content_type
        elif "/" in content_type and content_type[0] != "/":
            # applies to e.g text/plain
            return content_type
        # applies to e.g html, file.text
        return mimetypes.guess_type(" ."+content_type)[0]

    @classmethod
    def guess_type(cls, source, content_type=None):
        '''Guess content type from text source and another content type\n
        source - url, filepath, file object, etc\n
        content_type - string in form e.g 'text/', '.html', 
        'html', 'text/plain' or 'file.txt'''
        text_source = cls.source_to_text(source)
        source_content_type = cls.transform_content_type(content_type)
        # try content_type argument else guess from source
        if source_content_type:
            return source_content_type
        return cls.source_to_content_type(text_source)


    def get_file(self):
        '''Returns file object kept by this object'''
        self.file.seek(0)
        return self.file

    def get_file_copy(self):
        '''Returns copy of file kept by the object'''
        # its contents are copied to temp file
        temp_file = tempfile.TemporaryFile(mode='w+b')
        shutil.copyfileobj(self.file, temp_file)
        temp_file.seek(0)
        return temp_file

    def is_empty(self):
        '''Checks if underlying file object is empty'''
        self.file.seek(0, 2)
        return self.file.tell() == 0

    @staticmethod
    def open(source: str, *args, **kwargs) -> io.IOBase:
        '''Opens temporary file in binary mode\n
        source - url, filepath, file object, etc\n
        *args- optional arguments to pass to TemporaryFile()\n
        **kwagrs - optional arguments to pass to TemporaryFile()\n'''
        # files should always be opened in binary mode
        return tempfile.TemporaryFile(mode="w+b", *args, **kwargs)

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid\n
        source - url, filepath, file object, etc\n'''
        raise NotImplementedError()

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if data in source is accessible\n
        source - url, filepath, file object, etc\n'''
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
        '''Checks if source text was auto generated\n
        source - url, filepath, file object, etc\n'''
        if not isinstance(source, str):
            TypeError("source should be string not ", type(source))
        return Fetch_Base.unknown_source_prefix in source


    def read(self, *args, **kwagrs) -> str:
        '''Reads data located at file(where data is written)\n
        *args- optional arguments to pass to file.read()\n
        **kwagrs - optional arguments to pass to file.read()\n'''
        self.file.seek(0)
        return self.file.read(*args, **kwagrs)

    @classmethod
    def fetch(cls, source, *args, **kwagrs) -> str:
        '''Fetches and read data from source(url, filepath, etc)\n
        source - url, filepath, file object, etc\n
        '''
        raise NotImplementedError()

    def fetch_to_disc(self, source: str) -> str:
        '''Fetch data from source to file and return file object\n
        source - url, filepath, file object, etc'''
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

    def __del__(self):
        self.file.close()
