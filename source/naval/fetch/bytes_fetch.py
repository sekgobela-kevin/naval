from ast import Bytes
from io import BytesIO
from .file_fetch import File_Fetch


class Bytes_Fetch(File_Fetch):
    '''Fetches data from bytes'''
    def __init__(self, source, content_type=None, **kwargs):
        '''source - sequence of bytes(Bytes obect)\n
        content_type - content type for data in bytes\n
        **kwargs - optional keywords args to pass to base class(File_Fetch)
        '''
        bytes_file = BytesIO(source)
        super().__init__(bytes_file, content_type, **kwargs)

    @staticmethod
    def is_source_valid(source: str) -> bool:
        '''Checks if source is valid\n
        source - sequence of bytes(Bytes obect)\n'''
        # source should only be bytes not file object or file path
        # File_Fetch accepts also file object string(file path)
        return isinstance(source, bytes)

if __name__ == "__main__":
    fetch_obj = Bytes_Fetch(b"sequence of bytes", content_type=" .pdf")
    print(fetch_obj.read())
    # b'sequence of bytes'
    print(fetch_obj.get_content_type())
    # application/pdf