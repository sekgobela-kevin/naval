from io import IOBase
import tempfile
import mimetypes
import shutil

from ...utility.container import Container
from ..fetch.fetch_base import Fetch_Base

class Parse_Base():
    '''Base class for parsing fetch object into text, html or 
    container(sections)'''
    # content type for expected fetch object
    fetch_content_type = None
    # the higher priority value, the lower priority
    # parse class with lower priority is favoured when parsing
    # text parser for html file be used if no parser for html
    # html file is valid text which can be parsed by text parser
    # html parser should be have priority over text parser
    # priority can be increased by decreasing this value
    priority = 0

    def __init__(self, fetch_obj: Fetch_Base) -> None:
        '''fetch_obj - Object with data to parse. The 
        object should be created from Fetch_Base or its subclasses. For files,
        use File_Fetch class and for web use Web_Fetch class.'''
        self.fetch_obj = fetch_obj
        self.fetch_obj.request()
        # object to use to parse fetched data
        # its usually an object created by another library
        #self.doc = self.create_doc()
        self.doc = self.create_doc()
        # file object to store extracted text 
        self.text_file = self.create_file()
        # file object to store extracted HTML
        self.html_file = self.create_file()
        # files should always be opened in text mode
        # fetch object files be opened in binary mode

    def get_doc(self):
        '''Returns underlying document object'''
        return self.doc

    @classmethod
    def is_source_parsable(cls, source: str) -> bool:
        '''Checks if source can be parsed based on its mimetype\n
        source - file path or url'''
        if not isinstance(source, str):
            err_msg = "source should only be string"
            raise TypeError(err_msg, type(fetch_obj))   
        if not mimetypes.inited: mimetypes.init()
        fetch_type = mimetypes.guess_type(source)[0]
        if fetch_type:
            # "in" would allow to match only 'text' in text/html
            return cls.fetch_content_type in fetch_type
        return False 
        

    @classmethod
    def is_fetch_valid(cls, fetch_obj) -> bool:
        '''Checks if fetch object is valid. Source or bytes of 
        fetch object may be inspected. Its not guaranteed that
        fetch object will be parsed even if it may be valid'''
        if not isinstance(fetch_obj, Fetch_Base):
            err_msg = "fetch_obj is not created from Fetch_Base or its subclass"
            raise TypeError(err_msg, type(fetch_obj))
        return cls.is_source_parsable(fetch_obj.get_source())

    def create_file(self, *args, **kwarg) -> IOBase:
        '''Returns file object to stored parsed data\n
        *args, **kwarg - arguments to pass to TemporaryFile()/open()'''
        # files should always be opened in text mode
        return tempfile.TemporaryFile(mode="w+", *args, **kwarg)

    def is_file_empty(self, file):
        '''Cehcks if file object is empty'''
        file.seek(0,2)
        return file.tell() == 0
    
    
    def create_doc(self, *args, **kwarg):
        '''Return object to use when parsing fetch object contents.'''
        return object

    def text_to_file(self):
        '''Parses text and store it to self.text_file'''
        raise NotImplementedError

    def html_to_file(self):
        '''Parses html and store it to self.html_file'''
        raise NotImplementedError

    def get_text_file(self):
        '''Returns file kept by object'''
        return self.text_file

    def get_html_file(self):
        '''Returns file kept by object'''
        return self.html_file

    @staticmethod
    def get_file_copy(file_obj):
        '''Returns copy of file kept by the object'''
        # its contents are copied to temp file
        temp_file = tempfile.TemporaryFile(mode='w+')
        shutil.copyfileobj(file_obj, temp_file)
        temp_file.seek(0)
        return temp_file

    def get_text_file_copy(self):
        '''Returns copy file kept by object'''
        return self.get_file_copy(self.text_file)

    def get_html_file_copy(self):
        '''Returns copy of file kept by object'''
        return self.get_file_copy(self.html_file)
    
    def get_fetch(self):
        '''Returns fetch object'''
        return self.fetch_obj
    
    def get_title(self):
        '''Extracts title from fetch object'''
        raise NotImplementedError
    
    def get_text(self, *args, **kwargs) -> str or bytes:
        '''Retuns text version of fetch object\n
        *args, **kwargs - otional arguments to pass to file.read()'''
        if self.is_file_empty(self.text_file):
            self.text_to_file()
        self.text_file.seek(0)
        return self.text_file.read(*args, **kwargs)

    def get_html(self, *args, **kwargs) -> str:
        '''Retuns html version of fetch object\n
        *args, **kwargs - otional arguments to pass to file.read()'''
        if self.is_file_empty(self.html_file):
            self.html_to_file()
        self.html_file.seek(0)
        return self.html_file.read(*args, **kwargs)

    def get_container(self) -> Container:
        '''Retuns fetch object represented as container'''
        raise NotImplementedError

    @staticmethod
    def text_to_container(text) -> Container:
        '''Converts text to container(sections)'''

    @staticmethod
    def html_to_container(text) -> Container:
        '''Converts text to container(sections)'''

    def __del__(self):
        self.text_file.close()
        self.html_file.close()


if __name__ == "__main__":
    from ..fetch.master_fetch import Master_Fetch

    url = "https://realpython.com/beautiful-soup-web-scraper-python/"
    fetch_obj = Master_Fetch.get_fetch_object(url)
    parse_obj = Parse_Base(fetch_obj)
