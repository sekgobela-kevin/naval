from io import FileIO, IOBase
import unittest
import tempfile
from pynavy.crawler.fetch.file_fetch import File_Fetch


class Test_File_Fetch(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.file_path = __file__
        self.file_object = tempfile.TemporaryFile()
        self.fetch_obj = File_Fetch(self.file_object)

    def tearDown(self):
        self.file_object.close()

    def test_open(self):
        fetch_obj = File_Fetch(self.file_object)
        self.assertEqual(fetch_obj.open(self.file_object), self.file_object)
        with self.assertRaises(TypeError):
            # only str and file object allowed as source
            fetch_obj.open(44)   
        with self.assertRaises(FileNotFoundError):
            # "path to file" is not path to file
            fetch_obj.open("path to file")   

    def test_is_source_valid(self):
        self.assertTrue(File_Fetch.is_source_valid(self.file_object))
        self.assertTrue(File_Fetch.is_source_valid(__file__))
        # this is valid file path(relative)
        # "folder/path to file" is invalid(bad)
        self.assertTrue(File_Fetch.is_source_valid("path to file"))
        # this cant be a valid path
        self.assertFalse(File_Fetch.is_source_valid("path/%$to\/file\//"))
        with self.assertRaises(TypeError):
            # only str and file object allowed as source
            File_Fetch.is_source_valid(44)   


    def test_is_source_active(self):
        # file object is already active
        self.assertTrue(File_Fetch.is_source_active(self.file_object))
        # this file doesnt exists(inactive)
        self.assertFalse(File_Fetch.is_source_active("not_exists.file"))
        # this is file is active
        self.assertTrue(File_Fetch.is_source_active(self.file_path))
        with self.assertRaises(TypeError):
            # only str and file object allowed as source
            File_Fetch.is_source_active(44)   

    def test_fetch_to_disc(self):
        file_obj = self.fetch_obj.fetch_to_disc(self.fetch_obj.get_source())
        self.assertIsInstance(self.file_object, IOBase)