import io

from ..fetch.fetch_base import Fetch_Base
from .master_fetch import Master_Fetch

class Fetch(Fetch_Base, Master_Fetch):
    '''Main class for fetching data from source'''
    def __init__(self, source, *args, **kwargs):
        # create fetch object for source
        self.fetch_obj = self.get_fetch_object(source)
        super().__init__(source, *args, **kwargs)

    @classmethod
    def source_to_text(cls, source) -> str:
        '''Returns text version of source. e.g file object would
        return its path or file name'''
        return cls.source_to_text(source)

    def open(self, *args, **kwargs) -> io.IOBase:
        # then source arg refers to file object
        return self.fetch_obj.get_file()

    def is_source_valid(self, source: str) -> bool:
        '''Checks if source is valid\n
        source - url, file path, file object, etc'''
        return self.fetch_obj.is_source_valid(source)

    def is_source_active(self, source: str) -> bool:
        '''Checks if source is active\n
        source - url, file path, file object, etc'''
        return self.fetch_obj.is_source_active(source)

    def fetch_to_file(self, source: str, file: io.FileIO) -> str:
        '''Read raw data from source and save to file\n
        source - url, file path, file object, etc\n
        file - file like object to store data'''
        self.fetch_obj.fetch_to_file(source, file)
        return self.fetch_obj.get_file()

    def get_fetch(self):
        '''Returns underlying fetch object'''
        return self.fetch_obj

if __name__ == "__main__":
    fetch_obj = Fetch("https://www.tutorialspoint.com/")
    fetch_obj.request()
    print(fetch_obj.fetch())