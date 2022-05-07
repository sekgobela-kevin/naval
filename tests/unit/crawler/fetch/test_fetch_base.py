from io import FileIO, IOBase
import unittest
import tempfile
from src.pynavy.crawler.fetch.fetch_base import Fetch_Base


class Test_Fetch_Base(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.file_path = __file__
        self.file_object = tempfile.TemporaryFile()
        self.url = "www.example.com"

    def test_open(self):
        # this test is part of fetch_file
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        self.assertEqual(fetch_obj.open(self.file_object), self.file_object)
        with self.assertRaises(TypeError):
            # only str and file object allowed as source
            fetch_obj.open(44)   
        with self.assertRaises(ValueError):
            # ValueError be raised if path not pointing to file
            fetch_obj.open("path to file")   

    def test_get_file(self):
        fetch_obj = Fetch_Base(self.file_path)
        self.assertIsInstance(fetch_obj.get_file(), IOBase)
        fetch_obj = Fetch_Base(self.file_object)
        self.assertIsInstance(fetch_obj.get_file(), IOBase)
        self.assertEqual(fetch_obj.get_file(), self.file_object)

    def test_is_empty(self):
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        self.assertTrue(fetch_obj.is_empty())
        self.file_object.write(b'bytes')
        self.assertFalse(fetch_obj.is_empty())

    def test_is_source_valid(self):
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        with self.assertRaises(NotImplementedError):
            fetch_obj.is_source_valid(__file__)

    def test_is_source_active(self):
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        with self.assertRaises(NotImplementedError):
            fetch_obj.is_source_active(__file__)

    def test_get_unknown_source(self):
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        # expected to be different in each call
        self.assertNotEqual(fetch_obj.get_unknown_source(), 
        fetch_obj.get_unknown_source())
        # prefix should be the same
        self.assertIn(fetch_obj.unknown_source_prefix, 
        fetch_obj.get_unknown_source())


    def test_is_source_unknown(self):
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        # this source is unknown
        unknown_source = fetch_obj.get_unknown_source()
        self.assertTrue(fetch_obj.is_source_unknown(unknown_source))
        # __file__ is a known source that can be validated
        self.assertFalse(fetch_obj.is_source_unknown(__file__))

    def test_get_filename(self):
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        # temporary file source is unknown
        # unknown source one is created
        filename = fetch_obj.get_filename(self.file_object)
        self.assertTrue(fetch_obj.is_source_unknown(filename))
        # for string, the passed string should be returned
        filename = fetch_obj.get_filename(__file__)
        self.assertEqual(filename, __file__)

    def test_fetch(self):
        self.file_object.write(b'')
        fetch_obj = Fetch_Base(self.file_object)
        self.assertEqual(fetch_obj.fetch(), b'')
        # check ifeverything from file is being fetched
        self.file_object.write(b'bytes')
        self.assertEqual(fetch_obj.fetch(), b'bytes')
        # check if optional arguments passed to file.read()
        self.assertEqual(fetch_obj.fetch(2), b'by')

    def test_fetch_to_disc(self):
        fetch_obj = Fetch_Base(self.file_object)
        with self.assertRaises(NotImplementedError):
            fetch_obj.fetch_to_disc(fetch_obj.get_source())

    def test_request(self):
        fetch_obj = Fetch_Base(self.file_object)
        with self.assertRaises(NotImplementedError):
            fetch_obj.request()

    def test_close(self):
        fetch_obj = Fetch_Base(self.file_object)
        file_obj = fetch_obj.get_file()
        self.assertFalse(file_obj.closed)
        fetch_obj.close()
        self.assertTrue(file_obj.closed)




