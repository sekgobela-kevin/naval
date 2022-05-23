import io

from ..fetch.fetch_base import Fetch_Base
from .master_fetch import Master_Fetch

class Fetch(Fetch_Base, Master_Fetch):
    '''Main class for fetching data from source'''
    def __init__(self, source, *args, **kwargs):
        # create fetch object for source
        self.fetch_obj = self.get_fetch_object(source)
        super().__init__(source, *args, **kwargs)

    def open(self, *args, **kwargs) -> io.IOBase:
        '''Opens temporary file\n
        *args- optional arguments to pass to TemporaryFile() or open()\n
        **kwagrs - optional arguments to pass to TemporaryFile() or open()\n'''
        # then source arg refers to file object
        return self.fetch_obj.get_file()

    def is_source_valid(self, source: str) -> bool:
        '''Checks if source is valid'''
        return self.fetch_obj.is_source_valid(source)

    def is_source_active(self, source: str) -> bool:
        '''Checks if source is active'''
        return self.fetch_obj.is_source_active(source)

    def fetch_to_disc(self, source: str) -> str:
        '''Read raw data from source and save to file'''
        self.fetch_obj.fetch_to_disc(source)
        return self.fetch_obj.get_file()

    def get_fetch(self):
        '''Returns underlying fetch object'''
        return self.fetch_obj

if __name__ == "__main__":
    fetch_obj = Fetch("https://www.tutorialspoint.com/")
    fetch_obj.request()
    print(fetch_obj.fetch())