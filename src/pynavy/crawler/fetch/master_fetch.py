from io import FileIO
from typing import Type
from black import List

from ..fetch.file_fetch import File_Fetch
from ..fetch.web_fetch import Web_Fetch
from ..fetch.fetch_base import Fetch_Base


class Master_Fetch():
    '''Provide methods for fetching data from different sources.
    Acts as master for all fetch classes by deciding which fetch class
    source to use to fetch data. All methods are static.'''
    # stores fetch classes
    fetch_classes: List[Type[Fetch_Base]] = []

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid for any of fetch classes\n
        source - used for locating and fetching data(e.g file path, url)'''
        return any(map(lambda x: x.is_source_valid(source), Master_Fetch.fetch_classes))

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if source is active for all fetch classes\n
        source - used for locating and fetching data(e.g file path, url)'''
        return any(map(lambda x: x.is_source_active(source), Master_Fetch.fetch_classes))

    @staticmethod
    def fetch_class_exists(source: str) -> bool:
        '''Checks if fetch class for source exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        for fetch_class in Master_Fetch.fetch_classes:
            if fetch_class.is_source_valid(source):
                return True 
        return False

    @staticmethod
    def get_fetch_class(source: str) -> Type[Fetch_Base]:
        '''returns fetch class for source if exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        for fetch_class in Master_Fetch.fetch_classes:
            if fetch_class.is_source_valid(source):
                return fetch_class
        raise Exception(f"fetch class for source({source}) not found")

    @staticmethod
    def get_fetch_object(source: str, *args, **kwargs) -> Fetch_Base:
        '''returns fetch object for source if fetch class exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_class = Master_Fetch.get_fetch_class(source)
        return fetch_class(source, *args, **kwargs)

    @staticmethod
    def get_file(source: str, *args, **kwargs) -> FileIO:
        '''Returns file object from source(may be empty)\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_obj = Master_Fetch.get_fetch_object(source, *args, **kwargs)
        return fetch_obj.get_file()

    @staticmethod
    def fetch_to_disc(self, source: str, *args, **kwargs) -> FileIO:
        '''Fetches data from source and store to file\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_obj = Master_Fetch.get_fetch_object(source, *args, **kwargs)
        return fetch_obj.fetch_to_disc(source, *args, **kwargs)

    @staticmethod
    def fetch(source: str, *args, **kwargs) -> str or bytes:
        '''Fetch data from source\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_obj = Master_Fetch.get_fetch_object(source, *args, **kwargs)
        fetch_obj.close()
        return fetch_obj.fetch()

    @staticmethod
    def register_fetch_class(fetch_class: Type[Fetch_Base]) -> None:
        '''Registers class for fetching data from source'''
        if issubclass(fetch_class, Fetch_Base):
            TypeError(f"fetch_class({type(fetch_class)} should be subclass of \
            Fetch_Base")
        if fetch_class not in Master_Fetch.fetch_classes:
            Master_Fetch.fetch_classes.append(fetch_class)

# register fetch classes
Master_Fetch.register_fetch_class(File_Fetch)
Master_Fetch.register_fetch_class(Web_Fetch)

if __name__ == "__main__":
    url = 'http://docs.python.org/library/tempfile.html'
    fetch_obj = Master_Fetch()
    print(fetch_obj.is_source_valid(url))
    file_fetch = fetch_obj.get_fetch_object(__file__)
    file_fetch.request()
    print(len(file_fetch.fetch()))
