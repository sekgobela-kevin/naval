from io import FileIO, IOBase
import unittest
import tempfile
from naval.fetch.fetch import Fetch
from naval.fetch.fetch_base import Fetch_Base
from naval.fetch.file_fetch import File_Fetch


class Test_Fetch(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.file_path = __file__
        self.file_object = tempfile.TemporaryFile()
        self.file_object2 = open(self.file_path)
        self.fetch_obj = Fetch(self.file_object)

        self.html = "<div> division </div>"

    def tearDown(self):
        self.file_object.close()
        self.file_object2.close()
        self.fetch_obj.close()

    def test_source_to_text(self):
        self.assertEqual(Fetch.source_to_text(self.file_path), 
        self.file_path)
        with self.assertRaises(Exception):
            Fetch.source_to_text(self.html)
        Fetch.source_to_text(self.html, source_locates_data=False)

    def test_open(self):
        file_obj = self.fetch_obj.open(self.file_object)
        self.assertEqual(file_obj, self.file_object)
        file_obj.close()

    def test_is_source_valid(self):
        # is_source_valid() only checks if source is file
        self.assertTrue(Fetch.is_source_valid(self.file_object))
        self.assertTrue(Fetch.is_source_valid(__file__))
        self.assertFalse(Fetch.is_source_valid(self.html))
        valid = Fetch.is_source_valid(self.html, source_locates_data=False)
        self.assertTrue(valid)


    def test_is_source_active(self):
        # file object is already active
        self.assertTrue(Fetch.is_source_active(self.file_object))
        # this file doesnt exists(inactive)
        self.assertFalse(Fetch.is_source_active("not_exists.file"))
        self.assertFalse(Fetch.is_source_active(self.html))
        valid = Fetch.is_source_active(self.html, source_locates_data=False)
        self.assertTrue(valid)

    def test_fetch_to_file(self):
        self.fetch_obj.fetch_to_file(self.file_path, self.file_object)
        self.assertGreater(self.file_object.tell(), 0)

    def test_get_fetch_class(self):
        fetch_class = self.fetch_obj.get_fetch_class()
        self.assertEqual(fetch_class, File_Fetch)

if __name__ == '__main__':
    unittest.main()
