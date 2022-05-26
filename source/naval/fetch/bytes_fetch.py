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

if __name__ == "__main__":
    fetch_obj = Bytes_Fetch(b"sequence of bytes", content_type=" .pdf")
    print(fetch_obj.read())
    # b'sequence of bytes'
    print(fetch_obj.get_content_type())
    # application/pdf