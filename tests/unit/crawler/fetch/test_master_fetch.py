from io import FileIO, IOBase
import unittest
import tempfile
from src.pynavy.crawler.fetch.master_fetch import *


class Test_Master_Fetch(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.url = "https://www.google.com"
        self.url2 = "https://www.example.com"
        self.url3 = "https://www.google-test-url.com"
        self.url4 = "https://www.example-test-url.com"
        self.url5 = "www.google.com"
        self.file_path = __file__ 
        self.file_path2 = "/not_exists/file.txt" 
        self.file_obj = open(__file__, 'rb')

        # register fetch classes
        # dont remove this
        Master_Fetch.register_fetch_class(File_Fetch)
        Master_Fetch.register_fetch_class(Web_Fetch)
        
    def tearDown(self):
        self.file_obj.close()


    def test_is_source_valid(self):
        # test if it works for file paths
        self.assertTrue(Master_Fetch.is_source_valid(self.file_path))
        self.assertFalse(Master_Fetch.is_source_valid(self.file_path2))
        self.assertTrue(Master_Fetch.is_source_valid(self.file_obj))
        # test if it works for urls
        self.assertTrue(Master_Fetch.is_source_valid(self.url))
        self.assertTrue(Master_Fetch.is_source_valid(self.url4))
        self.assertFalse(Master_Fetch.is_source_valid(self.url5))
        # invalid argument shouldnt raise an error
        # it should rather be invalid
        self.assertFalse(Master_Fetch.is_source_valid([]))

    def test_is_source_active(self):
        # test if it works for file paths
        self.assertTrue(Master_Fetch.is_source_active(self.file_path))
        self.assertFalse(Master_Fetch.is_source_active(self.file_path2))
        self.assertTrue(Master_Fetch.is_source_active(self.file_obj))
        # test if it works for urls
        self.assertTrue(Master_Fetch.is_source_active(self.url))
        self.assertFalse(Master_Fetch.is_source_active(self.url4))
        self.assertFalse(Master_Fetch.is_source_active(self.url5))
        # invalid argument shouldnt raise an error
        # it should rather be invalid
        self.assertFalse(Master_Fetch.is_source_active([]))

    def test_fetch_class_exists(self):
        # check if fetch class is valid
        # it just checks if source is valid
        self.assertTrue(Master_Fetch.fetch_class_exists(self.file_path))
        self.assertTrue(Master_Fetch.fetch_class_exists(self.url))
        # this url is considered invalid, no fetch class for it
        self.assertFalse(Master_Fetch.fetch_class_exists(self.url5))
        # empty string is invalid, no fetch class for it
        self.assertFalse(Master_Fetch.fetch_class_exists(""))

    def test_get_fetch_class(self):
        # check if corresponding fetch class is returned
        fetch_class = Master_Fetch.get_fetch_class(self.file_path)
        self.assertTrue(fetch_class, File_Fetch)
        fetch_class = Master_Fetch.get_fetch_class(self.file_obj)
        self.assertTrue(fetch_class, File_Fetch)
        # error be raised if fetch class not found
        with self.assertRaises(Exception):
            self.assertTrue("")

    def test_get_fetch_object(self):
        # check if corresponding fetch class is returned
        fetch_object = Master_Fetch.get_fetch_object(self.file_path)
        self.assertIsInstance(fetch_object, File_Fetch)
        fetch_object.close()
        fetch_object = Master_Fetch.get_fetch_object(self.url)
        self.assertIsInstance(fetch_object, Web_Fetch)
        fetch_object.close()
        # error be raised if fetch class of object not found
        with self.assertRaises(Exception):
            self.assertTrue("")

    def test_get_file(self):
        file = Master_Fetch.get_file(self.file_path)
        # file is returned
        self.assertIsInstance(file, IOBase)
        # file should be open
        self.assertFalse(file.closed)
        file.close()

    def test_fetch(self):
        # check if data is fetched from source
        fetched = Master_Fetch.fetch(self.file_path)
        self.assertIsInstance(fetched, (str, bytes))
        # check if fetched data is not empty
        self.assertGreater(len(fetched), 0)

    def test_fetch_to_disc(self):
        # check if data is fetched from source to file in disc
        file = Master_Fetch.fetch_to_disc(self.url)
        self.assertIsInstance(file, IOBase)
        # check data was fetched to file
        self.assertGreater(len(file.read(10)), 0)
        file.close()

    def test_get_source(self):
        # valid string source is returned unchanged
        self.assertEqual(Master_Fetch.get_source(self.url), self.url)
        self.assertEqual(Master_Fetch.get_source(__file__), __file__)
        # file name of file object should be retured
        self.assertEqual(Master_Fetch.get_source(self.file_obj), __file__)
        with self.assertRaises(Exception):
            self.assertEqual(Master_Fetch.get_source(""), "")

    def test_register_fetch_class(self):
        # clear all existing fetch classes
        Master_Fetch.fetch_classes.clear()
        # fetch class for files shouldnt exists as its already cleared
        self.assertFalse(Master_Fetch.fetch_class_exists(self.file_path))
        Master_Fetch.register_fetch_class(File_Fetch)
        # fetch class should now exists
        self.assertTrue(Master_Fetch.fetch_class_exists(self.file_path))
        # this one wasnt registered
        self.assertFalse(Master_Fetch.fetch_class_exists(self.url))
        Master_Fetch.register_fetch_class(Web_Fetch)
        # now its registered
        self.assertTrue(Master_Fetch.fetch_class_exists(self.url))

    def test_deregister_fetch_classes(self):
        # web fetch class should exists
        self.assertTrue(Master_Fetch.fetch_class_exists(self.url))
        Master_Fetch.deregister_fetch_classes()
        # all fetch classes should be deregisted/cleared
        self.assertFalse(Master_Fetch.fetch_class_exists(self.file_path))
        self.assertFalse(Master_Fetch.fetch_class_exists(self.url))

    def test_fetch_class_registered(self):
        # web fetch class should exists
        self.assertTrue(Master_Fetch.fetch_class_registered(Web_Fetch))
        self.assertTrue(Master_Fetch.fetch_class_registered(File_Fetch))
        Master_Fetch.deregister_fetch_classes()
        # fetch shouldnt exists when deregistered
        self.assertFalse(Master_Fetch.fetch_class_registered(File_Fetch))

    

if __name__ == '__main__':
    unittest.main()
