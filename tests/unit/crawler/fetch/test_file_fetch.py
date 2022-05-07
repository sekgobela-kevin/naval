from io import FileIO, IOBase
import unittest
import tempfile
from src.pynavy.crawler.fetch.file_fetch import File_Fetch


class Test_File_Fetch(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.file_path = __file__
        self.file_object = tempfile.TemporaryFile()


    def test_open(self):
        # duplicate of this test exists in test_fetch_base.py
        self.file_object.write(b'')
        fetch_obj = File_Fetch(self.file_object)
        self.assertEqual(fetch_obj.open(self.file_object), self.file_object)
        with self.assertRaises(TypeError):
            # only str and file object allowed as source
            fetch_obj.open(44)   
        with self.assertRaises(ValueError):
            # ValueError be raised if path not pointing to file
            fetch_obj.open("path to file")   

    def test_is_source_valid(self):
        self.file_object.write(b'')
        fetch_obj = File_Fetch(self.file_object)
        self.assertTrue(fetch_obj.is_source_valid(self.file_object))
        self.assertTrue(fetch_obj.is_source_valid(__file__))
        # not valid, not pointing to valid file
        self.assertFalse(fetch_obj.is_source_valid("path to file"))
        with self.assertRaises(TypeError):
            # only str and file object allowed as source
            fetch_obj.is_source_valid(44)   


    def test_is_source_active(self):
        self.file_object.write(b'')
        fetch_obj = File_Fetch(self.file_object)
        # is_source_valid() and is_source_active() should return same results
        # reason is that is_source_active() uses is_source_active()
        self.assertEqual(fetch_obj.is_source_valid(self.file_object),
        fetch_obj.is_source_active(self.file_object))
        self.assertEqual(fetch_obj.is_source_valid("path to file"),
        fetch_obj.is_source_active("path to file"))
        with self.assertRaises(TypeError):
            # only str and file object allowed as source
            fetch_obj.is_source_active(44)   

    def test_fetch_to_disc(self):
        fetch_obj = File_Fetch(self.file_object)
        file_obj = fetch_obj.fetch_to_disc(fetch_obj.get_source())
        self.assertIsInstance(file_obj, IOBase)