from io import BytesIO, IOBase, StringIO
import os, tempfile

import unittest
from naval.utility.files import *

class Test_File_Functions(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = os.path.join("samples", "sample_file.txt")
        self.string_file = StringIO()
        self.file_path2 = "not_exists.txt"
        self.bytes_file = BytesIO()

    def tearDown(self):
        self.string_file.close()
        self.bytes_file.close()
        try:
            os.unlink(self.file_path2)
        except FileNotFoundError:
            pass

    def test_is_binary(self):
        self.assertTrue(is_binary(self.bytes_file))
        self.assertFalse(is_binary(self.string_file))

    def test_is_text(self):
        self.assertFalse(is_text(self.bytes_file))
        self.assertTrue(is_text(self.string_file))

    def test_is_file_object(self):
        self.assertTrue(is_file_object(self.string_file))
        with tempfile.TemporaryFile() as f:
            self.assertTrue(is_file_object(f))
        self.assertFalse(is_file_object("file"))

    def test_get_file_object(self):
        # the same file object should be returned
        self.assertEqual(get_file_object(self.string_file), self.string_file)
        file_obj = get_file_object(self.file_path2, mode="w")
        self.assertIsInstance(file_obj, IOBase)
        # check if file object is not closed
        self.assertFalse(file_obj.closed)
        file_obj.close()
        with self.assertRaises(TypeError):
            get_file_object([90])

    def test_copy_file(self):
        self.string_file.write("string")
        with self.assertRaises(TypeError):
            # cant write string to bytes file
            copy_file(self.string_file, self.bytes_file)
        
        self.setUp()
        copy_file(BytesIO(b"bytes"), self.bytes_file)
        # check if file was written
        self.assertGreater(self.bytes_file.tell(), 0)

        self.setUp()
        # let hope this wont cause permission error
        copy_file(self.file_path, self.file_path2)
        with open(self.file_path2) as f:
            # check if file was created and written
            f.seek(0,2)
            self.assertGreater(f.tell(), 0)
        
        with self.assertRaises(TypeError):
            copy_file(self.file_path, [90])

if __name__ == '__main__':
    unittest.main()
