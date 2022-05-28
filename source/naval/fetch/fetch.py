import io

from ..fetch.fetch_base import Fetch_Base
from .master_fetch import Master_Fetch

class Fetch(Fetch_Base):
    '''Main class for fetching data from source'''
    def __init__(self, source, content_type=None, source_locates_data=True):
        # create fetch object for source
        self.fetch_obj = Master_Fetch.get_fetch_object(source, source_locates_data)
        super().__init__(source, content_type)
    
    @classmethod
    def source_to_text(cls, source) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        return Master_Fetch.source_to_text(source)

    @classmethod
    def is_source_valid(cls, source: str) -> bool:
        '''Checks if source is valid\n
        source - url, file path, file object, etc'''
        return Master_Fetch.is_source_valid(source)

    @classmethod
    def is_source_active(cls, source: str) -> bool:
        '''Checks if source is active\n
        source - url, file path, file object, etc'''
        return Master_Fetch.is_source_active(source)

    @classmethod
    def fetch_to_file(cls, source: str, file: io.FileIO) -> str:
        '''Read raw data from source and save to file\n
        source - url, file path, file object, etc\n
        file - file like object to store data'''
        return Master_Fetch.fetch_to_file(source, file)

    def get_fetch(self):
        '''Returns underlying fetch object'''
        return self.fetch_obj

if __name__ == "__main__":
    fetch_obj = Fetch("https://www.tutorialspoint.com/")
    fetch_obj.request()
    print(fetch_obj.fetch())