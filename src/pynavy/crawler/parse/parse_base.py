from io import IOBase
import tempfile
from ...utility.container import Container
from ..fetch.fetch_base import Fetch_Base

class Parse_Base():
    '''Base class for parsing fetch object into text, html or 
    container(sections)'''
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

    def create_file(self, *args, **kwarg) -> IOBase:
        '''Returns file object to stored parsed data'''
        return tempfile.TemporaryFile(mode="w+")

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

    def is_fetch_valid():
        '''Checks if contents of fetch object can be parsed'''
        raise NotImplementedError

    def get_html_file(self):
        '''Returns file kept by object'''
        return self.file

    def get_html_file(self):
        '''Returns file kept by object'''
        return self.html_file
    
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
