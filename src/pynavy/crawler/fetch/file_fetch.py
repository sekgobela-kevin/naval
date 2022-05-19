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
        # get string source in case source is file object
        # super().__init__() will set file object as source
        # this line will extract name of file object as
        # if it fails then unkown source get created from timestamp
        self._source = self.get_filename(source)

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
        # get string version of source incase source is file object
        source = File_Fetch.get_filename(source)
        # its possible that data in file not be readable
        # os.access() may be better
        return os.path.isfile(source)

    def fetch_to_disc(self, source: str) -> str:
        '''Fetch data from source to file and return file object'''
        # no need to fetch data is already in file
        return self.file


if __name__ == "__main__":

    string = tempfile.TemporaryFile()
    string.write(b"jhhh")
    print(os.path.isfile(__file__))
    crawl_obj = File_Fetch(string)
    print(len(crawl_obj))
    #print(crawl_obj[0].get_text())
    print(crawl_obj.is_source_active(crawl_obj.get_source()))
    print(crawl_obj.request())
