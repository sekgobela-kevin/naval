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


    @classmethod
    def is_source_valid(cls, source, source_locates_data=True) -> bool:
        '''Checks if source is valid for any of fetch classes'''
        for fetch_class in cls.fetch_classes:
            # handle execption in case a source not supported
            # Web_Fetch does not support file object
            try:
                if source_locates_data == fetch_class.source_locates_data:
                    isvalid =  fetch_class.is_source_valid(source)
                    if isvalid: return True
            except(ValueError, TypeError):
                pass
        return False


    @classmethod
    def is_source_active(cls, source, source_locates_data=True) -> bool:
        '''Checks if source is active for all fetch classes'''
        for fetch_class in cls.fetch_classes:
            # handle execption in case a source not supported
            # Web_Fetch does not support file object
            try:
                if source_locates_data == fetch_class.source_locates_data:
                    isactive =  fetch_class.is_source_active(source)
                    if isactive: return True
            except(ValueError, TypeError):
                pass
        return False

    @staticmethod
    def fetch_class_exists(source, source_locates_data=True) -> bool:
        '''Checks if fetch class for source exists'''
        return Master_Fetch.is_source_valid(source, source_locates_data)

    @staticmethod
    def get_fetch_class(source, source_locates_data=True) -> Type[Fetch_Base]:
        '''returns fetch class for source if exists'''
        fetch_classes = []
        for fetch_class in Master_Fetch.fetch_classes:
            try:
                if source_locates_data == fetch_class.source_locates_data:
                    if fetch_class.is_source_valid(source):
                        fetch_classes.append(fetch_class)
            except(ValueError, TypeError):
                continue
        if fetch_classes: return fetch_classes[0]
        raise Exception(f"fetch class for source({source}) not found")

    @staticmethod
    def get_fetch_object(source, source_locates_data=True, **kwargs) -> Fetch_Base:
        '''returns fetch object for source if fetch class exists'''
        # check if source is active before creating fetch objetc
        if not Master_Fetch.is_source_valid(source, source_locates_data):
            raise Exception(f"source({source}) is not fetchable(no fetch class)")
        if not Master_Fetch.is_source_active(source, source_locates_data):
            raise Exception(f"source({source}) is not fetchable(not active)")
        fetch_class = Master_Fetch.get_fetch_class(source, source_locates_data)
        return fetch_class(source, **kwargs)

    @staticmethod
    def get_file(source, source_locates_data=True, **kwargs) -> FileIO:
        '''Returns file with fetched data'''
        fetch_obj = Master_Fetch.get_fetch_object(source, 
        source_locates_data, **kwargs)
        fetch_obj.request()
        return fetch_obj.get_file_copy()

    @staticmethod
    def fetch_to_file(source, file: FileIO, source_locates_data=True, 
    **kwargs) -> FileIO:
        '''Fetches data from source and store to file'''
        fetch_class = Master_Fetch.get_fetch_class(source, source_locates_data)
        fetch_class.fetch_to_file(source, file, **kwargs)
        return file

    @staticmethod
    def fetch(source, source_locates_data=True, **kwargs) -> bytes:
        '''Fetches data from source and return bytes'''
        fetch_class = Master_Fetch.get_fetch_class(source, source_locates_data)
        return fetch_class.fetch(source, **kwargs)

    @staticmethod
    def source_to_text(source, source_locates_data=True, **kwargs) -> str:
        '''Returns text version of source'''
        fetch_class = Master_Fetch.get_fetch_class(source, source_locates_data)
        return fetch_class.source_to_text(source, **kwargs)

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
