from io import FileIO, IOBase
import mimetypes
import unittest
import tempfile
from naval.fetch.fetch_base import Fetch_Base


class Test_Fetch_Base(unittest.TestCase):
    def setUp(self):
        # carefull not to overide this file
        self.file_path = __file__
        self.file_object = tempfile.TemporaryFile()
        self.file_object2 = open(self.file_path)
        self.url = "www.example.com"

        self.fetch_obj = Fetch_Base(self.file_object)
        self.fetch_obj2 = Fetch_Base(self.file_path)
    
    def tearDown(self):
        self.file_object.close()
        self.file_object2.close()

    def test_get_source(self):
        self.assertEqual(self.fetch_obj.get_source(), self.file_object)
        self.assertEqual(self.fetch_obj2.get_source(), self.file_path)

    def test_source_to_text(self):
        self.assertEqual(Fetch_Base.source_to_text(self.file_path), 
        self.file_path)
        source_text = Fetch_Base.source_to_text(self.file_object)
        self.assertTrue(Fetch_Base.is_source_unknown(source_text))

    def test_get_source_text(self):
        self.assertEqual(self.fetch_obj2.get_source_text(), 
        Fetch_Base.source_to_text(self.file_path))

    def test_transform_content_type(self):
        content_type = Fetch_Base.transform_content_type('text/')
        self.assertEqual(content_type, 'text/')
        content_type = Fetch_Base.transform_content_type('text/plain')
        self.assertEqual(content_type, 'text/plain')
        content_type = Fetch_Base.transform_content_type('.html')
        self.assertEqual(content_type, mimetypes.guess_type(' .html')[0])
        content_type = Fetch_Base.transform_content_type('pdf')
        self.assertEqual(content_type, mimetypes.guess_type(' .pdf')[0])
        content_type = Fetch_Base.transform_content_type('.docx')
        self.assertEqual(content_type, mimetypes.guess_type(' .docx')[0])

    def test_source_to_content_type(self):
        self.assertEqual(Fetch_Base.source_to_content_type(self.file_object),
        None)
        self.assertEqual(Fetch_Base.source_to_content_type(self.file_path),
        mimetypes.guess_type(self.file_path)[0])
        self.assertEqual(Fetch_Base.source_to_content_type("file.docx"), 
        mimetypes.guess_type(' .docx')[0])
        self.assertEqual(Fetch_Base.source_to_content_type("file.html"), 
        mimetypes.guess_type(' .html')[0])
        self.assertEqual(Fetch_Base.source_to_content_type('erdfx'), None)

    def test_guess_type(self):
        self.assertEqual(Fetch_Base.guess_type(self.file_object), None)
        self.assertEqual(Fetch_Base.guess_type(self.file_path),
        mimetypes.guess_type(self.file_path)[0])
        self.assertEqual(Fetch_Base.guess_type(self.file_object, 
        ".docx"), mimetypes.guess_type(' .docx')[0])
        self.assertEqual(Fetch_Base.guess_type(self.file_path, 
        "file"), mimetypes.guess_type(self.file_path)[0])

    def test_get_content_type(self):
        self.assertEqual(Fetch_Base(self.file_path).get_content_type(), 
        Fetch_Base.source_to_content_type(self.file_path))

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

    def test_read(self):
        self.assertEqual(self.fetch_obj.read(), b'')
        # check if everything from file is being fetched
        self.fetch_obj.get_file().write(b'bytes')
        self.assertEqual(self.fetch_obj.read(), b'bytes')
        # check if optional arguments passed to file.read()
        self.assertEqual(self.fetch_obj.read(2), b'by')

    def test_fetch(self):
        with self.assertRaises(NotImplementedError):
            Fetch_Base.fetch(self.fetch_obj.get_source())

    def test_fetch_to_disc(self):
        with self.assertRaises(NotImplementedError):
            self.fetch_obj.fetch_to_disc(self.fetch_obj.get_source())

    def test_request(self):
        with self.assertRaises(NotImplementedError):
            self.fetch_obj.request()

    def test_close(self):
        file_obj = self.fetch_obj.get_file()
        self.assertFalse(file_obj.closed)
        self.fetch_obj.close()
        self.assertTrue(file_obj.closed)


if __name__ == '__main__':
    unittest.main()
