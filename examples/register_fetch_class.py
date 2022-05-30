from io import BytesIO, IOBase, StringIO
import os
from naval.fetch import Fetch_Base
import naval

# setup file paths to use later
pdf_file_path = os.path.join("files", "sample_file.pdf")
html_file_path = os.path.join("files", "sample_file.html")
text_file_path = os.path.join("files", "sample_file.txt")





# This fetch class fetches data from file object and file path
# It was created in examples/extending_fetch.py
# Let register it so that it works with extract_text()

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


# let first deregister all existing fetch classes
naval.deregister_fetch_classes()

# error will be raised(no fetch class)
#naval.create_fetch_object(pdf_file_path)

# same with Fetch class(no fetch class)
#fetch_obj = naval.Fetch(pdf_file_path)

# methods including extract_text() wont work
# they depend on fetch classes to fetch data



################################
# LET REGISTER OUR FETCH CLASS #
################################

naval.register_fetch_class(Fetch_File)

# let create fetch objetc from .create_fetch_object()
# and Fetch class.
fetch_obj = naval.create_fetch_object(pdf_file_path)
fetch_obj = naval.Fetch(pdf_file_path)
# realise that error wasnt raised


# fetch class register and deregister functions
###############################################

# registers fetch class
naval.register_fetch_class(Fetch_File)
# deregisters fetch class
naval.deregister_fetch_class(Fetch_File)
# returns True if fetch class is registered
naval.fetch_class_registered(Fetch_File)
# returns refererance registered fetch classes
naval.get_registered_fetch_classes()
# dregistered all fetch classes
naval.deregister_fetch_classes()

# only deregisters fetch classes passed
naval.deregister_fetch_classes([Fetch_File])



# Let extract text from pdf file
naval.register_fetch_class(Fetch_File)
text = naval.extract_text(pdf_file_path)
#print(text)
