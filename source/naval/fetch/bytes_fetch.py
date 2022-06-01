from io import BytesIO, IOBase, FileIO
from .fetch_base import Fetch_Base


class Bytes_Fetch(Fetch_Base):
    '''Fetches data from bytes'''
    # specifies if source points to data
    source_locates_data = False

    def __init__(self, source, content_type=None, **kwargs):
        '''source - sequence of bytes(Bytes obect)\n
        content_type - content type for data in bytes\n
        **kwargs - optional keywords args to pass to base class(File_Fetch)
        '''
        super().__init__(source, content_type, **kwargs)

    @classmethod
    def is_source_valid(cls, source: str) -> bool:
        '''Checks if source is valid\n
        source - sequence of bytes(Bytes obect)\n'''
        # source should only be bytes not file object or file path
        # File_Fetch accepts also file object string(file path)
        return isinstance(source, bytes)

    @classmethod
    def source_to_text(cls, source) -> str:
        return ascii(source)

    @classmethod
    def is_source_active(cls, source: str) -> bool:
        '''Checks if source is valid\n
        source - sequence of bytes(Bytes obect)\n'''
        return cls.is_source_valid(source)

    @classmethod
    def fetch_to_file(cls, source: str, file: FileIO) -> str:
        if not cls.is_source_valid(source):
            raise TypeError(f"source should be bytes not ", type(source))
        file.write(source)


if __name__ == "__main__":
    fetch_obj = Bytes_Fetch(b"sequence of bytes", content_type=" .pdf")
    fetch_obj.request()
    print(fetch_obj.read())
    # b'sequence of bytes'
    print(fetch_obj.get_content_type())
    # application/pdf