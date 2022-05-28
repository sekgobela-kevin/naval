from io import FileIO, IOBase
import unittest
import tempfile
from naval.fetch.fetch import Fetch
from naval.fetch.fetch_base import Fetch_Base


class Test_Fetch(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.file_path = __file__
        self.file_object = tempfile.TemporaryFile()
        self.file_object2 = open(self.file_path)
        self.fetch_obj = Fetch(self.file_object)

    def tearDown(self):
        self.file_object.close()
        self.file_object2.close()
        self.fetch_obj.close()

    def test_source_to_text(self):
        self.assertEqual(Fetch.source_to_text(self.file_path), 
        self.file_path)

    def test_open(self):
        file_obj = self.fetch_obj.open(self.file_object)
        self.assertIsInstance(file_obj, IOBase)
        file_obj.close()

    def test_is_source_valid(self):
        # is_source_valid() only checks if source is file
        self.assertTrue(Fetch.is_source_valid(self.file_object))
        self.assertTrue(Fetch.is_source_valid(__file__))

    def test_is_source_active(self):
        # file object is already active
        self.assertTrue(Fetch.is_source_active(self.file_object))
        # this file doesnt exists(inactive)
        self.assertFalse(Fetch.is_source_active("not_exists.file"))

    def test_fetch_to_file(self):
        self.fetch_obj.fetch_to_file(self.file_path, self.file_object)
        self.assertGreater(self.file_object.tell(), 0)

    def test_get_fetch(self):
        fetch_obj = self.fetch_obj.get_fetch()
        self.assertIsInstance(fetch_obj, Fetch_Base)

if __name__ == '__main__':
    unittest.main()
