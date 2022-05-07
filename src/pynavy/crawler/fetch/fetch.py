from io import FileIO
from typing import Type
from black import List

from ..fetch.file_fetch import File_Fetch
from ..fetch.web_fetch import Web_Fetch
from ..text.text import Text

# type annotations
fetch_class_types = File_Fetch or Web_Fetch


class Fetch():
    '''Provide methods for fetching data from different sources'''
    # stores fetch classes
    fetch_classes: List[File_Fetch] = [File_Fetch, Web_Fetch]

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid for any of fetch classes\n
        source - used for locating and fetching data(e.g file path, url)'''
        return any(map(lambda x: x.is_source_valid(source), Fetch.fetch_classes))

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if source is active for all fetch classes\n
        source - used for locating and fetching data(e.g file path, url)'''
        return any(map(lambda x: x.is_source_active(source), Fetch.fetch_classes))

    @staticmethod
    def fetch_class_exists(source: str) -> bool:
        '''Checks if fecth class for source exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        for fetch_class in Fetch.fetch_classes:
            if fetch_class.is_source_valid(source):
                return True 
        return False

    @staticmethod
    def get_fetch_class(source: str) -> Type[fetch_class_types]:
        '''returns fetch class for source if exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        for fetch_class in Fetch.fetch_classes:
            if fetch_class.is_source_valid(source):
                return fetch_class
        raise Exception(f"fecth class for source({source}) not found")

    @staticmethod
    def get_fetch_object(source: str, *args, **kwargs) -> fetch_class_types:
        '''returns fetch object for source if fetch class exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_class = Fetch.get_fetch_class(source)
        return fetch_class(source, *args, **kwargs)

    @staticmethod
    def get_file(source: str, *args, **kwargs) -> FileIO:
        '''Returns file object from source(may be empty)\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_obj = Fetch.get_fetch_object(source, *args, **kwargs)
        return fetch_obj.get_file()

    @staticmethod
    def fetch_to_disc(self, source: str, *args, **kwargs) -> FileIO:
        '''Fetches data from source and store to file\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_obj = Fetch.get_fetch_object(source, *args, **kwargs)
        return fetch_obj.fetch_to_disc(source, *args, **kwargs)

    @staticmethod
    def fetch(source: str, *args, **kwargs) -> str or bytes:
        '''Fetch data from source\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_obj = Fetch.get_fetch_object(source, *args, **kwargs)
        fetch_obj.close()
        return fetch_obj.fetch()


if __name__ == "__main__":
    fetch_obj = Fetch()
    print(fetch_obj.is_source_valid("cder"+__file__))
    file_fetch = fetch_obj.get_fetch_object(__file__)
    print(len(file_fetch.fetch()))
