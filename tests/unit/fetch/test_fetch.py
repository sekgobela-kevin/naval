from io import FileIO, IOBase, BytesIO
import unittest
import tempfile, os

from naval.fetch.fetch import Fetch
from naval.fetch.fetch_base import Fetch_Base
from naval.fetch.file_fetch import File_Fetch
from naval.fetch.string_fetch import String_Fetch

from .common_tests import Common_Tests


class Test_Fetch(Common_Tests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = os.path.join("samples", "sample_file.txt")
        cls.source2 = BytesIO()
        cls.source3 = "<div> division </div>"

        cls.fetch_object = Fetch(cls.source)
        cls.fetch_object2 = Fetch(cls.source2)
        cls.fetch_object3 = Fetch(cls.source3, source_locates_data=False,
        content_type="html")
        # let see if theres an error(fetch class not found)
        cls.fetch_object3.request()

        cls.html = "<div> division </div>"

    def test_source_to_text(self):
        self.assertEqual(self.fetch_object.source_to_text(self.source), 
        self.source)
        self.fetch_object.source_to_text(self.html, source_locates_data=False)


    def test_is_source_valid(self):
        # is_source_valid() only checks if source is file
        self.assertTrue(self.fetch_object.is_source_valid(self.source2))
        self.assertTrue(self.fetch_object.is_source_valid(self.source))
        self.assertFalse(self.fetch_object.is_source_valid(self.html))
        valid = self.fetch_object.is_source_valid(self.html, source_locates_data=False)
        self.assertTrue(valid)


    def test_is_source_active(self):
        # file object is already active
        self.assertTrue(self.fetch_object.is_source_active(self.source2))
        # this file doesnt exists(inactive)
        self.assertFalse(self.fetch_object.is_source_active("not_exists.file"))
        self.assertFalse(self.fetch_object.is_source_active(self.html))
        isvalid = self.fetch_object.is_source_active(self.html, 
        source_locates_data=False)
        self.assertTrue(isvalid)

    def test_fetch_to_file(self):
        self.fetch_object.fetch_to_file(self.source, self.source2)
        self.assertGreater(self.source2.tell(), 0)

    def test_get_fetch_class(self):
        fetch_class = self.fetch_object.get_fetch_class()
        self.assertEqual(fetch_class, File_Fetch)

if __name__ == '__main__':
    unittest.main()
