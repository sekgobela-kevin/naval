import helper
# folders in src to path
# src_to_path() add folder in src to path
helper.src_to_path(__file__)

import unittest
from crawler.text.metadata import Metadata


class TestMetadata(unittest.TestCase):

    def test_get_metadata(self):
        metadata_obj = Metadata({"index": 3})
        self.assertEqual(metadata_obj.get_metadata(), {"index": 3})
    
    def test_set_metadata(self):
        metadata_obj = Metadata()
        metadata_obj.set_metadata({"index": 0})
        self.assertEqual(metadata_obj.get_metadata(), {"index": 0})
        with self.assertRaises(ValueError):
            metadata_obj.set_metadata(10)

    def test_get_data(self):
        metadata_obj = Metadata({"index": 2})
        self.assertEqual(metadata_obj.get_data("index"), 2)

    def test_add_data(self):
        metadata_obj = Metadata()
        metadata_obj.add_data("index", 2)
        self.assertEqual(metadata_obj.get_data("index"), 2)
        with self.assertRaises(KeyError):
            metadata_obj.get_data("type")

    def test_data_exists(self):
        metadata_obj = Metadata({"index": 2})
        self.assertTrue(metadata_obj.data_exists("index"))
        self.assertFalse(metadata_obj.data_exists("type"))

    def test_remove_data(self):
        metadata_obj = Metadata()
        metadata_obj.add_data("index", 2)
        self.assertTrue(metadata_obj.data_exists("index"))
        metadata_obj.remove_data("index")
        self.assertFalse(metadata_obj.data_exists("index"))

    def test_get_metadata_size(self):
        metadata_obj = Metadata({"index": 2, "length": 4000})
        self.assertEqual(metadata_obj.get_metadata_size(), 2)

    def test_clear_metadata(self):
        metadata_obj = Metadata({"index": 2, "length": 4000})
        self.assertEqual(metadata_obj.get_metadata_size(), 2)
        metadata_obj.clear_metadata()
        self.assertEqual(metadata_obj.get_metadata_size(), 0)

if __name__ == '__main__':
    unittest.main()