from io import IOBase
import os
import unittest
from pynavy.utility.files import *

class Test_File_Functions(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = __file__
        self.file_object = open(self.file_path)
        self.file_path2 = "file.txt"
        self.file_object2 = open(self.file_path2, "w+")

    def tearDown(self):
        self.file_object.close()
        self.file_object2.close()
        try:
            os.unlink("file.txt")
        except FileNotFoundError:
            pass

    def test_is_binary(self):
        file_obj = open(self.file_path2, "wb")
        self.assertTrue(is_binary(file_obj))
        self.assertFalse(is_binary(self.file_object))
        file_obj.close()

    def test_is_text(self):
        file_obj = open(self.file_path2, "wb")
        self.assertFalse(is_text(file_obj))
        self.assertTrue(is_text(self.file_object))
        file_obj.close()

    def test_get_file_object(self):
        # the same file object should be returned
        self.assertEqual(get_file_object(self.file_object), self.file_object)
        file_obj = get_file_object(self.file_path2, mode="w")
        self.assertIsInstance(file_obj, IOBase)
        # check if file object is not closed
        self.assertFalse(file_obj.closed)
        file_obj.close()
        with self.assertRaises(TypeError):
            get_file_object([90])

    def test_copy_file(self):
        copy_file(self.file_object, self.file_object2)
        # file like objects shouldnt be closed
        self.assertFalse(self.file_object.closed)
        self.assertFalse(self.file_object2.closed)
        # check if file was written
        self.assertGreater(self.file_object2.tell(), 0)
        copy_file(self.file_path, self.file_path2)
        file_obj = open(self.file_path2)
        # check if file was created and written
        file_obj.seek(0,2)
        self.assertGreater(file_obj.tell(), 0)
        file_obj.close()
        with self.assertRaises(TypeError):
            copy_file(self.file_path, [90])

if __name__ == '__main__':
    unittest.main()
