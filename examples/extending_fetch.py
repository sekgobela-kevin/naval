from io import BytesIO, IOBase, StringIO
import os
from naval.fetch import Fetch_Base


pdf_file_path = os.path.join("files", "sample_file.pdf")
html_file_path = os.path.join("files", "sample_file.html")
text_file_path = os.path.join("files", "sample_file.txt")



class File_Object_Fetch(Fetch_Base):
    '''fetchs data from file object'''

    def __init__(self, source, content_type=None, *args, **kwargs):
        super().__init__(source, content_type, *args, **kwargs)

    @classmethod
    def is_source_valid(cls, source):
        '''Checks if source is file object'''
        # you can also validate source based on other condition
        # just return true if you dont want to validate source
        return isinstance(source, IOBase)

    @classmethod
    def fetch_to_file(cls, source, dest_file):
        '''Read contents of source(file object) to destination file'''
        # both source and dest_file are file objects
        # source is the file with 
        if not cls.is_source_valid(source):
            err_msg = "source is not supported(should be file like object)"
            raise TypeError(err_msg, type(source))
        source.seek(0)
        dest_file.writelines(source)



fetch_obj = File_Object_Fetch(BytesIO(b"sequence of character"))
# .request() fetches data from the file
# for url, it performs a request
fetch_obj.request()
#print(fetch_obj.read())

# error will be raised
# TypeError: ('source argument is not file like object', <class 'str'>)
#fetch_obj = File_Object_Fetch("sequence of character")






class Disc_File_Fetch(Fetch_Base):
    '''fetches data from file in file system(disc)'''

    def __init__(self, source, content_type=None, *args, **kwargs):
        if not self.is_source_valid(source):
            raise TypeError(f"source{source} is not supported", type(source))
        super().__init__(source, content_type, *args, **kwargs)

    @classmethod
    def is_source_valid(cls, source):
        '''Checks if source is file object'''
        if isinstance(source, (str, bytes)):
            return os.path.isfile(source)
        # just return if you dont want to validate source
        return False

    @classmethod
    def fetch_to_file(cls, source, dest_file):
        '''Read contents of source(file path) to destination file'''
        # dest_file is a file object
        # source is a file path
        with open(source, mode="rb") as file:
            file.seek(0)
            dest_file.writelines(file)


fetch_obj = Disc_File_Fetch(text_file_path)
fetch_obj.request()
#print(fetch_obj.read().decode())




# This fetch class fetches data from file object and file path
# It will handle both of them

class Fetch_File(Fetch_Base):
    '''fetches data from file in path or filr object'''

    def __init__(self, source, content_type=None, *args, **kwargs):
        if not self.is_source_valid(source):
            err_msg = "source needs to be file path or file like object"
            raise TypeError(f"source{source} is not supported", type(source))
        super().__init__(source, content_type, *args, **kwargs)

    @classmethod
    def is_file_object(cls, source):
        # file objects inherits IOBase
        return isinstance(source, IOBase)

    @classmethod
    def is_file_path(cls, source):
        # validate file path
        if isinstance(source, (str, bytes)):
            return os.path.isfile(source)
        return False

    @classmethod
    def is_source_valid(cls, source):
        '''Checks if source is valid file object or file path'''
        # source becomes valid if is a file path or file like object
        return cls.is_file_object(source) or cls.is_file_path(source)

    @classmethod
    def fetch_to_file(cls, source, dest_file):
        '''Read contents of source(file path) to destination file'''
        if cls.is_file_path(source):
            # open file if source is file object
            file = open(source, mode="rb")
        elif cls.is_file_object(source):
            # source is already file object
            file = source
        else:
            # else the source is not valid(invalid file path or wrong type)
            err_msg = "source needs to be valid file path or file like object"
            raise TypeError(err_msg, type(source))
        file.seek(0)
        dest_file.writelines(file)


# supply file path
fetch_obj = Fetch_File(text_file_path)
fetch_obj.request()
#print(fetch_obj.read().decode())

# supply file like object
fetch_obj = Fetch_File(BytesIO(b"This comes from file like object"))
fetch_obj.request()
print(fetch_obj.read().decode())
# 'This comes from file like object'


# what about registering our fetch classes
# making them work with extract_text() or Fetch class
