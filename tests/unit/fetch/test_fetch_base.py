from io import FileIO, IOBase
import unittest
import tempfile
from pynavy.crawler.fetch.fetch_base import Fetch_Base


class Test_Fetch_Base(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.file_path = __file__
        self.file_object = tempfile.TemporaryFile()
        self.url = "www.example.com"
        self.fetch_obj = Fetch_Base(self.file_object)
        self.file_object.truncate(0)
    
    def tearDown(self):
        self.file_object.close()

    def test_open(self):
        # temporary file should be opened
        # source shouldnt even be checked
        self.fetch_obj.open(44).close()
        self.fetch_obj.open("not exists file.pdf").close()

    def test_get_file(self):
        # check if is instance of IOBase
        self.assertIsInstance(self.fetch_obj.get_file(), IOBase)

    def test_is_empty(self):
        # file is empty on start of test
        self.assertTrue(self.fetch_obj.is_empty())
        self.fetch_obj.get_file().write(b'bytes')
        # somethng have been written
        self.assertFalse(self.fetch_obj.is_empty())

    def test_is_source_valid(self):
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
        self.assertEqual(self.fetch_obj.fetch(), b'')
        # check if everything from file is being fetched
        self.fetch_obj.get_file().write(b'bytes')
        self.assertEqual(self.fetch_obj.fetch(), b'bytes')
        # check if optional arguments passed to file.read()
        self.assertEqual(self.fetch_obj.fetch(2), b'by')

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




