from io import BytesIO, FileIO, IOBase
from .fetch_base import Fetch_Base


class String_Fetch(Fetch_Base):
    '''Fetches data from string'''
    # specifies if source points to data
    source_locates_data = False

    def __init__(self, source:str, content_type:str=None, **kwargs):
        '''source - sequence of characters(string)\n
        content_type - content type for data in string\n
        **kwargs - optional keywords args to pass to base class(File_Fetch)
        '''
        super().__init__(source, content_type, **kwargs)

    @classmethod
    def is_source_valid(cls, source: str) -> bool:
        '''Checks if source is valid\n
        source - sequence of characters(string)\n'''
        # source should only be string not file object
        # File_Fetch accepts also file object
        return isinstance(source, str)

    @classmethod
    def fetch_to_file(cls, source: str, file: FileIO) -> str:
        if not cls.is_source_valid(source):
            raise TypeError(f"source should be string not ", type(source))
        file.write(source.encode())



if __name__ == "__main__":
    fetch_obj = String_Fetch("This is string", content_type=" .txt")
    fetch_obj.request()
    print(fetch_obj.read())
    # b'This is string' 
    print(fetch_obj.get_content_type())
    # text/plain

