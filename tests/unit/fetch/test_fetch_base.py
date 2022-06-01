from io import BytesIO, FileIO, IOBase
import mimetypes
import unittest

from naval.fetch.fetch_base import Fetch_Base
from .common_tests import Common_Tests


class Fetch_Base_Test(Fetch_Base):    
    # class for testing Fetch_Base class
    def __init__(self, source, content_type=None, **kwargs):
        super().__init__(source, content_type, **kwargs)

    @classmethod
    def is_source_valid(cls, source: str) -> bool:
        return True

    @classmethod
    def fetch_to_file(cls, source: str, file: FileIO) -> str:
        file.write(b"something")


class Test_Fetch_Base(Common_Tests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = "valid test source"
        cls.source2 = "valid test source2"

        cls.fetch_object = Fetch_Base_Test(cls.source)
        cls.fetch_object2 = Fetch_Base_Test(cls.source2)


    def test_source_to_content_type(self):
        self.assertEqual(self.fetch_object.source_to_content_type("file.xfpx"),
        None)
        self.assertEqual(self.fetch_object.source_to_content_type("file.docx"), 
        mimetypes.guess_type(' .docx')[0])
        self.assertEqual(self.fetch_object.source_to_content_type("file.html"), 
        mimetypes.guess_type(' .html')[0])

    def test_guess_type(self):
        self.assertEqual(self.fetch_object.guess_type("file.dyys"), None)
        self.assertEqual(self.fetch_object.guess_type("file.html"),
        "text/html")
        self.assertEqual(self.fetch_object.guess_type("file.docx", 
        ".docx"), mimetypes.guess_type(' .docx')[0])
        self.assertEqual(self.fetch_object.guess_type("file.txt", 
        "file"), "text/plain")


if __name__ == '__main__':
    unittest.main()
