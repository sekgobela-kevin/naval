import io

from ..fetch.fetch_base import Fetch_Base
from .master_fetch import Master_Fetch



def get_fetch_class(source, source_locates_data=True):
    fetch_class = Master_Fetch.get_fetch_class(
        source,
        source_locates_data=source_locates_data
    )
    return fetch_class

class Fetch(Fetch_Base):
    '''Main class for fetching data from source'''
    def __init__(self, source, source_locates_data=True, content_type=None):
        '''source - url, file path or gile object, etc\n
        source_locates_data(optional) - true if source is resource locator 
        e.g url, file path, default True.\n
        content_type(optional) - content type of data to be fetched. E.g 
        html, .html or text/html. Default is None'''
        # create fetch object for source
        self.fetch_class = get_fetch_class(source, source_locates_data)

        # this was taken from Fetch_Base __init__()
        # super().__init__() would raise errors sometimes
        # it doesnt support source_locates_data
        self._source = source
        self._source_text = self.source_to_text(source, 
        source_locates_data=source_locates_data)

        assert isinstance(self._source_text, str), self._source_text
        self.content_type = self.guess_type(source, 
        source_locates_data = source_locates_data)
        
        self.file = self.open(source, source_locates_data=source_locates_data)

    @classmethod
    def open(cls, source: str, source_locates_data=True, 
    *args, **kwargs) -> io.IOBase:
        '''Opens file file for storing fetched data\n
        source - url, filepath, file object, etc\n
        *args, **kwagrs - optional arguments to pass to open() function\n'''
        # files should always be opened in binary mode
        fetch_class = get_fetch_class(source, source_locates_data)
        return fetch_class.open(source, *args, **kwargs)

    
    @classmethod
    def source_to_text(cls, source, source_locates_data=True) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        fetch_class = get_fetch_class(source, source_locates_data)
        return fetch_class.source_to_text(source)


    @classmethod
    def source_to_content_type(cls, source, source_locates_data=True):
        '''Return content type of source(url, filepath, etc)\n
        source - url, filepath, file object, etc\n'''
        fetch_class = get_fetch_class(source, source_locates_data)
        return fetch_class.source_to_content_type(source)


    @classmethod
    def guess_type(cls, source, content_type=None, source_locates_data=True):
        '''Guess content type from text source and another content type\n
        source - url, filepath, file object, etc\n
        content_type - string in form e.g 'text/', '.html', 
        'html', 'text/plain' or 'file.txt'''
        fetch_class = get_fetch_class(source, source_locates_data)
        return fetch_class.guess_type(source)


    @classmethod
    def is_source_valid(cls, source, source_locates_data=True) -> bool:
        '''Checks if source is valid\n
        source - url, file path, file object, etc'''
        return Master_Fetch.is_source_valid(source, source_locates_data)

    @classmethod
    def is_source_active(cls, source, source_locates_data=True) -> bool:
        '''Checks if source is active\n
        source - url, file path, file object, etc'''
        return Master_Fetch.is_source_active(source, source_locates_data)

    @classmethod
    def fetch_to_file(cls, source, file: io.IOBase, source_locates_data=True):
        '''Fetch data from source to file and return file object\n
        source - url, filepath, file object, etc'''
        fetch_class = get_fetch_class(source, source_locates_data)
        return fetch_class.fetch_to_file(source, file)

    def get_fetch_class(self):
        '''Returns underlying fetch class of the object'''
        return self.fetch_class

if __name__ == "__main__":
    fetch_obj = Fetch("https://www.tutorialspoint.com/")
    fetch_obj.request()
    print(fetch_obj.fetch())
