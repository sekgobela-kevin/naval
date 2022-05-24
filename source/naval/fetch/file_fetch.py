import mimetypes
from ..fetch.fetch_base import Fetch_Base

import tempfile
import os, sys, io
import random

class File_Fetch(Fetch_Base):
    '''Provide methods for fetching data from file'''
    def __init__(self, source, content_type=None, *args, **kwargs):
        '''source - file path or file like object\n
        *args- optional arguments to pass to file.open()\n
        **kwagrs - optional arguments to pass to file.open()\n
        '''
        super().__init__(source, content_type, *args, **kwargs)

    @classmethod
    def source_to_text(cls, source) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        return cls.get_filename(source)

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
            if File_Fetch.is_source_valid(source):
                return open(source, mode="rb", *args, **kwargs)
            else:
                raise ValueError(f"source({source}) not pointing to valid file")
        # then source arg refers to file object
        return source

    @staticmethod
    def is_file_path_valid(filePath):
        if not os.access(filePath, os.W_OK):
            try:
                open(filePath, 'w').close()
                os.unlink(filePath)
                return True
            except OSError:
                return False
        return True
    
    @staticmethod
    def is_source_valid(source: str or io.IOBase) -> bool:
        '''Checks if source is valid'''
        if not isinstance(source, (str, io.IOBase)):
            raise TypeError("file should be file obj or string not ", type(source))
        if isinstance(source, io.IOBase):
            # file object is valid on its own
            return True
        elif File_Fetch.is_source_unknown(source):
            # source was autotimatially created
            # it was validated before it got created
            return True
        # if all the above fails, then source might be file path
        return File_Fetch.is_file_path_valid(source)

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if data in source is accessible'''
        if not isinstance(source, (str, io.IOBase)):
            raise TypeError("file should be file obj or string not ", type(source))
        if isinstance(source, io.IOBase):
            # file object is active on its own
            return True
        # get string version of source incase source is file object
        source = File_Fetch.get_filename(source)
        # its possible that data in file not be readable
        # os.access() may be better
        return os.path.isfile(source)

    @classmethod
    def get_filename(cls, source: io.IOBase or str):
        '''Creates filename from path or file object\n
        source - file object or path to file'''
        if not isinstance(source, (str, io.IOBase)):
            TypeError("source should be file obj or string not ", type(source))
        if isinstance(source, str): 
            return source
        elif "name" in dir(source):
            if isinstance(source.name, (str)):
                return source.name
        return cls.get_unknown_source()

    @classmethod
    def fetch_to_file(cls, source: str, file: io.FileIO) -> str:
        '''Fetch data from source to file and return file object\n
        source - file path or file like object\n
        file - file like object to store data'''
        source_file = cls.open(source)
        source_file.seek(0)
        # its not worth to write to same file
        # this checks if source and file are not same based on filename
        if cls.get_filename(source) != cls.get_filename(file):
            file.writelines(source_file)
            # close file if its not file like object
            if not isinstance(source, io.IOBase):
                source_file.close()
        return file

    def request(self, *args, **kwarg) -> io.IOBase:
        '''Read data from file path and return file object'''
        # file already has data
        # no need to request for data
        return self.file


if __name__ == "__main__":

    string = tempfile.TemporaryFile()
    string.write(b"jhhh")
    print(os.path.isfile(__file__))
    fetch_obj = File_Fetch(__file__)
    print(fetch_obj.is_source_active(fetch_obj.get_source()))
    print(fetch_obj.get_source_text())
    print(fetch_obj.get_content_type())
