from io import BytesIO, FileIO, IOBase
import unittest
import tempfile

from naval.fetch.web_fetch import Web_Fetch
from naval.fetch.file_fetch import File_Fetch
from naval.fetch.string_fetch import String_Fetch
from naval.fetch.master_fetch import Master_Fetch

from naval.utility import files


class Test_Master_Fetch(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.url = "https://www.google.com"
        self.url2 = "https://www.example.com"
        self.url3 = "https://www.google-test-url.com"
        self.url4 = "https://www.example-test-url.com"
        self.url5 = "www.google.com"
        self.file_path = __file__ 
        self.file_path2 = "file.txt" 
        self.file_obj = open(__file__, 'rb')
        self.text = "this is text"

        # register fetch classes
        # dont remove this
        Master_Fetch.register_fetch_class(File_Fetch)
        Master_Fetch.register_fetch_class(Web_Fetch)
        Master_Fetch.register_fetch_class(String_Fetch)
        
    def tearDown(self):
        self.file_obj.close()


    def test_is_source_valid(self):
        # test if it works for file paths
        self.assertTrue(Master_Fetch.is_source_valid(self.file_path))
        self.assertFalse(Master_Fetch.is_source_valid(self.text))
        # String_Fetch should match
        self.assertTrue(Master_Fetch.is_source_valid(self.text, 
        source_locates_data=False))

    def test_is_source_active(self):
        # test if it works for file paths
        self.assertTrue(Master_Fetch.is_source_active(self.file_path))
        self.assertTrue(Master_Fetch.is_source_active(self.file_obj))
        # self.file_path2 is valid but not active
        # error shouldnt be raised
        self.assertFalse(Master_Fetch.is_source_active(self.file_path2))
        # applies to String_Fetch
        self.assertFalse(Master_Fetch.is_source_active(self.text))
        self.assertTrue(Master_Fetch.is_source_active(self.text, 
        source_locates_data=False))

    def test_fetch_class_exists(self):
        # check if fetch class is valid
        # it just checks if source is valid
        self.assertTrue(Master_Fetch.fetch_class_exists(self.file_path))
        # empty string is invalid, no fetch class for it
        self.assertFalse(Master_Fetch.fetch_class_exists(""))
        # applies to String_Fetch
        self.assertFalse(Master_Fetch.fetch_class_exists(self.text))
        self.assertTrue(Master_Fetch.fetch_class_exists(self.text, 
        source_locates_data=False))


    def test_get_fetch_class(self):
        # check if corresponding fetch class is returned
        fetch_class = Master_Fetch.get_fetch_class(self.file_path)
        self.assertEqual(fetch_class, File_Fetch)
        fetch_class = Master_Fetch.get_fetch_class(self.file_obj)
        self.assertEqual(fetch_class, File_Fetch)
        # applies to String_Fetch
        fetch_class = Master_Fetch.get_fetch_class(
            self.file_path, 
            source_locates_data=False)
        self.assertEqual(fetch_class, String_Fetch)

    def test_get_fetch_object(self):
        # check if corresponding fetch class is returned
        fetch_object = Master_Fetch.get_fetch_object(self.file_path)
        self.assertIsInstance(fetch_object, File_Fetch)
        fetch_object.close()
        fetch_object = Master_Fetch.get_fetch_object(
            self.file_path, 
            source_locates_data=False
        )
        self.assertIsInstance(fetch_object, String_Fetch)
        # error be raised if fetch class of object not found
        with self.assertRaises(Exception):
            self.assertTrue(Master_Fetch.get_fetch_object(""))

    def test_get_file(self):
        with Master_Fetch.get_file(self.file_path) as file:
            # file is returned
            self.assertTrue(files.is_file_object(file))
            # file should be open
            self.assertFalse(file.closed)
            file.close()

    def test_fetch(self):
        # check if data is fetched from source
        fetched = Master_Fetch.fetch(self.file_path)
        self.assertIsInstance(fetched, (str, bytes))
        # check if fetched data is not empty
        self.assertGreater(len(fetched), 0)

    def test_fetch_to_file(self):
        file_obj = BytesIO()
        # check if data is fetched from source to file in disc
        Master_Fetch.fetch_to_file(self.file_path, file_obj)
        # check data was fetched to file
        self.assertGreater(file_obj.tell(), 0)
        file_obj.close()

    def test_source_to_text(self):
        # valid string source is returned unchanged
        self.assertEqual(Master_Fetch.source_to_text(self.url), self.url)
        self.assertEqual(Master_Fetch.source_to_text(__file__), __file__)
        # file name of file object should be retured
        self.assertEqual(Master_Fetch.source_to_text(self.file_obj), __file__)
        with self.assertRaises(Exception):
            self.assertEqual(Master_Fetch.source_to_text(""), "")

    def test_register_fetch_class(self):
        # clear all existing fetch classes
        Master_Fetch.fetch_classes.clear()
        # fetch class for files shouldnt exists as its already cleared
        self.assertFalse(Master_Fetch.fetch_class_exists(self.file_path))
        Master_Fetch.register_fetch_class(File_Fetch)
        # fetch class should now exists
        self.assertTrue(Master_Fetch.fetch_class_exists(self.file_path))

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
