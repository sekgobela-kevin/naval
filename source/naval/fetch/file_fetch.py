import mimetypes
from ..fetch.fetch_base import Fetch_Base
from ..utility import directories
from ..utility import files
from .. import sources

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


    @classmethod
    def is_file_path_valid(cls, filePath):
        # file_ext = directories.get_file_extension(filePath)
        # if not (os.sep in filePath or file_ext):
        #     # path is invalid without path seperator or extension
        #     # prevent matching of ordinary strings
        #     return False
        if not os.access(filePath, os.W_OK):
            try:
                open(filePath, 'w').close()
                os.unlink(filePath)
                return True
            except OSError:
                return False
        return True

    @classmethod
    def is_file_object(cls, source):
        # file objects inherits IOBase
        return files.is_file_object(source)

    @classmethod
    def is_file_path(cls, source):
        # validate file path
        if isinstance(source, (str, bytes)):
            if os.path.isfile(source):
                return True
            return sources.is_local_file(source)
        else:
            return False

    @classmethod
    def is_source_valid(cls, source):
        '''Checks if source is valid file object or file path'''
        # source becomes valid if is a file path or file like object
        # only existing file paths are valid
        # its harder to know if str or bytes file path
        # imagine 'employees' file, who could know if thats a file path
        # but 'employees.txt' can be detected as it has extension
        return cls.is_file_object(source) or os.path.isfile(source)

    @classmethod
    def is_source_active(cls, source):
        '''Checks if source is active file object or file path'''
        if cls.is_file_path(source):
            return os.path.isfile(source)
        elif cls.is_file_object(source):
            return True
        else:
            err_msg = f"source({source}) is not valid file path or file like object"
            raise TypeError(err_msg)

    @classmethod
    def fetch_to_file(cls, source, dest_file):
        '''Read contents of source(file path) to destination file'''
        # dest_file is expected to be binary
        if cls.is_file_path(source):
            with open(source, mode="rb") as f:
                dest_file.writelines(f)
        elif cls.is_file_object(source):
            # source is already file object
            # copy its contents to dest_file
            source.seek(0)
            for line in source:
                # handle exception if files opended in different modes
                # writing bytes to text file would raise errors
                try:
                    dest_file.write(line)
                except TypeError:
                    dest_file.write(line.encode(encoding="utf-8"))
        else:
            # else the source is not valid(invalid file path or wrong type)
            err_msg = f"source({source}) is not valid file path or file like object"
            raise TypeError(err_msg)


    @classmethod
    def get_filename(cls, source: io.IOBase or str):
        '''Creates filename from path or file object\n
        source - file object or path to file'''
        if cls.is_file_path(source): 
            return source
        elif cls.is_file_object(source):
            try:
                return source.name
            except AttributeError:
                # file like object without name
                # its likely to be StringIO or BytesIO
                return cls.get_unknown_source()
        else:
            err_msg = f"source({source}) is not valid file path or file like object"
            raise TypeError(err_msg)


if __name__ == "__main__":

    string = tempfile.TemporaryFile()
    string.write(b"jhhh")
    print(os.path.isfile(__file__))
    fetch_obj = File_Fetch(__file__)
    print(fetch_obj.is_source_active(fetch_obj.get_source()))
    print(fetch_obj.get_source_text())
    print(fetch_obj.get_content_type())
