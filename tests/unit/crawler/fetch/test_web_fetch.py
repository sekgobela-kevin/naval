from io import FileIO, IOBase
import unittest
import tempfile
from pynavy.crawler.fetch.web_fetch import Web_Fetch


class Test_Web_Fetch(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.url = "https://www.google.com"
        self.url2 = "https://www.example.com"
        self.url3 = "https://www.google-test-url.com"
        self.url4 = "https://www.example-test-url.com"
        self.url5 = "www.google.com"
        self.file_path = __file__
        self.fetch_obj = Web_Fetch(self.url)

    def test_open(self):
        # this should only create and return file object
        temp_file = Web_Fetch.open(self.url)
        self.assertIsInstance(temp_file, IOBase)
        temp_file.close()
        temp_file = Web_Fetch.open(self.url2)
        self.assertIsInstance(temp_file, IOBase)
        temp_file.close()
        # argumets arent validated as they are never used
        temp_file = Web_Fetch.open(334)
        self.assertIsInstance(temp_file, IOBase)
        temp_file.close()

    def test_is_source_valid(self):
        # both should be valid, they are valid urls
        self.assertTrue(Web_Fetch.is_source_valid(self.url))
        self.assertTrue(Web_Fetch.is_source_valid(self.url2))
        self.assertTrue(Web_Fetch.is_source_valid(self.url3))
        # both should be invalid, they are not urls
        self.assertFalse(Web_Fetch.is_source_valid(__file__))
        self.assertFalse(Web_Fetch.is_source_valid("path to file"))
        # this should be corrected
        # method considers it invalid but its valid
        self.assertFalse(Web_Fetch.is_source_valid("www.google.com"))
        with self.assertRaises(TypeError):
            # url should only be string
            Web_Fetch.is_source_valid(44)   


    def test_is_source_active(self):
        # the two are valid and active
        self.assertTrue(Web_Fetch.is_source_active(self.url))
        self.assertTrue(Web_Fetch.is_source_active(self.url2))
        # the two are valid but not active
        self.assertFalse(Web_Fetch.is_source_active(self.url3))
        self.assertFalse(Web_Fetch.is_source_active(self.url4))
        with self.assertRaises(TypeError):
            # url should only be string
            Web_Fetch.is_source_active(44)   

    def test_fetch_to_disc(self):
        file_obj = self.fetch_obj.get_file()
        file_obj.write(b'')
        new_file_obj = self.fetch_obj.fetch_to_disc(self.url)
        # check data was added to the file
        self.assertFalse(self.fetch_obj.is_empty())
        # check if it returns file object
        self.assertIsInstance(new_file_obj, IOBase)
        with self.assertRaises(TypeError):
            # url should only be a string
            self.fetch_obj.fetch_to_disc({})
