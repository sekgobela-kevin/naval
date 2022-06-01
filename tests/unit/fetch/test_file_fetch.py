from io import BytesIO, FileIO, IOBase
import os
import unittest

from naval.fetch.file_fetch import File_Fetch
from .common_tests import Common_Tests



class Test_File_Fetch(Common_Tests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = os.path.join("samples", "sample_file.txt")
        cls.source2 = BytesIO()
        cls.source3 =  os.path.join("samples", "sample_file")

        cls.fetch_object = File_Fetch(cls.source)
        cls.fetch_object2 = File_Fetch(cls.source2)

    def test_source_to_text(self):
        self.assertEqual(self.fetch_object.source_to_text(self.source), 
        self.source)
        source2_text = self.fetch_object.source_to_text(self.source2)
        self.assertTrue(self.fetch_object.is_source_unknown(source2_text))

    def test_is_source_valid(self):
        # is_source_valid() only checks if source is file
        self.assertTrue(self.fetch_object.is_source_valid(self.source))
        self.assertTrue(self.fetch_object.is_source_valid(self.source2))
        # "path to file" may be a file path but does not exists
        self.assertFalse(self.fetch_object.is_source_valid("path to file"))
        # this cant be a valid path
        self.assertFalse(self.fetch_object.is_source_valid("path/%$to\/file\//"))


    def test_is_source_active(self):
        # file object is already active
        self.assertTrue(self.fetch_object.is_source_active(self.source))
        # this file doesnt exists(inactive)
        self.assertFalse(self.fetch_object.is_source_active("not_exists.file"))
        # file object is active on its own
        self.assertTrue(self.fetch_object.is_source_active(self.source2))

    def test_is_source_unknown(self):
        with BytesIO() as f:
            # source text for memory file object is not known
            # it doesnt have .name attribute
            self.assertTrue(self.fetch_object.is_source_unknown(f))
        self.assertFalse(self.fetch_object.is_source_unknown(self.source))


if __name__ == '__main__':
    unittest.main()
    import sys
    print(sys.path)
