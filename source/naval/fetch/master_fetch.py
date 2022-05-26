from io import FileIO

from typing import Set, Type
from typing import List

from ..fetch.fetch_base import Fetch_Base
from ..fetch.file_fetch import File_Fetch
from ..fetch.web_fetch import Web_Fetch
from ..fetch.bytes_fetch import Bytes_Fetch
from ..fetch.string_fetch import String_Fetch


class Master_Fetch():
    '''Provide methods for fetching data from different sources.
    Acts as master for all fetch classes by deciding which fetch class
    source to use to fetch data. All methods are static.'''
    # stores fetch classes
    fetch_classes: Set[Type[Fetch_Base]] = set()

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid for any of fetch classes\n
        source - used for locating and fetching data(e.g file path, url)'''
        def callback(fetch_class):
            # handle execption in case a source not supported
            # Web_Fetch does not support file object
            try:
                return fetch_class.is_source_valid(source)
            except(ValueError, TypeError):
                return False
        return any(map(callback, Master_Fetch.fetch_classes))

    @staticmethod
    def is_source_active(source: str) -> bool:
        '''Checks if source is active for all fetch classes\n
        source - used for locating and fetching data(e.g file path, url)'''
        # source could only be active if already valid
        # so error is raised
        if not Master_Fetch.is_source_valid(source):
            raise Exception(f"source({source}) is invalid")
        def callback(fetch_class):
            # handle execption in case a source not supported
            # Web_Fetch does not support file object
            try:
                return fetch_class.is_source_active(source)
            except(ValueError, TypeError):
                return False
        return any(map(callback, Master_Fetch.fetch_classes))

    @staticmethod
    def fetch_class_exists(source: str) -> bool:
        '''Checks if fetch class for source exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        return Master_Fetch.is_source_valid(source)

    @staticmethod
    def get_fetch_class(source: str) -> Type[Fetch_Base]:
        '''returns fetch class for source if exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        for fetch_class in Master_Fetch.fetch_classes:
            # some sources arent supported by all fetch classes
            try:
                if fetch_class.is_source_valid(source):
                    return fetch_class
            except(ValueError, TypeError):
                continue
        raise Exception(f"fetch class for source({source}) not found")

    @staticmethod
    def get_fetch_object(source: str, *args, **kwargs) -> Fetch_Base:
        '''returns fetch object for source if fetch class exists\n
        source - used for locating and fetching data(e.g file path, url)'''
        # check if source is active before creating fetch objetc
        if not Master_Fetch.is_source_active(source):
            raise Exception(f"source({source}) is not active")
        fetch_class = Master_Fetch.get_fetch_class(source)
        return fetch_class(source, *args, **kwargs)

    @staticmethod
    def get_file(source: str, *args, **kwargs) -> FileIO:
        '''Returns temporary file object from source\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_obj = Master_Fetch.get_fetch_object(source, *args, **kwargs)
        return fetch_obj.get_file_copy()

    @staticmethod
    def fetch_to_file(source: str, file: FileIO, *args, **kwargs) -> FileIO:
        '''Fetches data from source and store to file\n
        source - used for locating and fetching data(e.g file path, url)\n
        file - file like object to store data'''
        fetch_class = Master_Fetch.get_fetch_class(source, *args, **kwargs)
        fetch_class.fetch_to_file(source, file, *args, **kwargs)
        return file

    @staticmethod
    def fetch(source: str, *args, **kwargs) -> str or bytes:
        '''Fetch data from source\n
        source - used for locating and fetching data(e.g file path, url)'''
        fetch_class = Master_Fetch.get_fetch_class(source, *args, **kwargs)
        return fetch_class.fetch(source)

    @staticmethod
    def source_to_text(source, *args, **kwargs) -> str:
        '''Returns text version of source\n
        source - str(file path, url, etc), None or file object'''
        fetch_class = Master_Fetch.get_fetch_class(source, *args, **kwargs)
        return fetch_class.source_to_text(source)

    @staticmethod
    def register_fetch_class(fetch_class: Type[Fetch_Base]) -> None:
        '''Registers class for fetching data from source'''
        # fetch_class needs to inherit Fetch_Base
        if not issubclass(fetch_class, Fetch_Base):
            raise TypeError(f"fetch_class subclass of Fetch_Base",
            fetch_class)
        Master_Fetch.fetch_classes.add(fetch_class)
    
    @staticmethod
    def fetch_class_registered(fetch_class: Type[Fetch_Base]) -> bool:
        '''Checks if fetch class is registered'''
        # fetch_class needs to inherit Fetch_Base
        if not issubclass(fetch_class, Fetch_Base):
            raise TypeError(f"fetch_class subclass of Fetch_Base",
            fetch_class)
        return fetch_class in Master_Fetch.fetch_classes

    @staticmethod
    def deregister_fetch_class(fetch_class: Type[Fetch_Base]) -> None:
        '''Registers class for fetching data from source'''
        # fetch_class needs to inherit Fetch_Base
        if not issubclass(fetch_class, Fetch_Base):
            raise TypeError(f"fetch_class subclass of Fetch_Base",
            fetch_class)
        if Master_Fetch.fetch_class_registered(fetch_class):
            Master_Fetch.fetch_classes.remove(fetch_class)

    @staticmethod
    def deregister_fetch_classes():
        '''Deregisters fetch class'''
        Master_Fetch.fetch_classes.clear()


# register fetch classes
Master_Fetch.register_fetch_class(File_Fetch)
Master_Fetch.register_fetch_class(Web_Fetch)
Master_Fetch.register_fetch_class(String_Fetch)
Master_Fetch.register_fetch_class(Bytes_Fetch)

if __name__ == "__main__":
    url = 'http://docs.python.org/library/tempfile.html'
    fetch_obj = Master_Fetch()
    print(fetch_obj.is_source_valid(url))
    file_fetch = fetch_obj.get_fetch_object(__file__)
    file_fetch.request()
    print(len(file_fetch.fetch()))
