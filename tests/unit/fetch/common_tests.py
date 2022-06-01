from io import BytesIO, FileIO, IOBase
import mimetypes, tempfile, os

from naval.fetch.fetch_base import Fetch_Base
from naval.utility import files


class Common_Tests():
    @classmethod
    def setUpClass(cls):
        cls.source: ...
        cls.source2: ...
        cls.source3: ...

        cls.fetch_object: Fetch_Base
        cls.fetch_object2: Fetch_Base
        cls.fetch_object3: Fetch_Base
    

    @classmethod
    def tearDownClass(cls):
        cls.fetch_object.close()
        cls.fetch_object2.close()

    def setUp(self):
        self.fetch_object.clear()
        self.fetch_object2.clear()

    def test_get_source(self):
        self.assertEqual(self.fetch_object.get_source(), self.source)
        self.assertEqual(self.fetch_object2.get_source(), self.source2)

    def test_source_to_text(self):
        # source is already string(no conversion needed)
        #self.assertEqual(self.fetch_object.source_to_text("source"), 
        #"source")
        pass

    def test_get_source_text(self):
        self.assertEqual(self.fetch_object.get_source_text(), 
        self.fetch_object.source_to_text(self.source))

    def test_transform_content_type(self):
        content_type = self.fetch_object.transform_content_type('text/')
        self.assertEqual(content_type, 'text/')
        content_type = self.fetch_object.transform_content_type('text/plain')
        self.assertEqual(content_type, 'text/plain')
        content_type = self.fetch_object.transform_content_type('.html')
        self.assertEqual(content_type, mimetypes.guess_type(' .html')[0])
        content_type = self.fetch_object.transform_content_type('pdf')
        self.assertEqual(content_type, mimetypes.guess_type(' .pdf')[0])
        content_type = self.fetch_object.transform_content_type('.docx')
        self.assertEqual(content_type, mimetypes.guess_type(' .docx')[0])

    def test_source_to_content_type(self):
        pass

    def test_guess_type(self):
        pass

    def test_get_content_type(self):
        self.assertEqual(self.fetch_object.get_content_type(), 
        self.fetch_object.source_to_content_type(self.source))

    # def test_open(self):
    #     # temporary file should be opened
    #     # source shouldnt even be checked
    #     self.fetch_object.open(44).close()
    #     self.fetch_object.open("not exists file.pdf").close()

    def test_get_file(self):
        # check if is instance of IOBase
        file_object = self.fetch_object.get_file()
        self.assertTrue(files.is_file_object(file_object))

    def test_is_empty(self):
        # file is empty on start of test
        self.assertTrue(self.fetch_object.is_empty())
        self.fetch_object.get_file().write(b'bytes')
        # somethng have been written
        self.assertFalse(self.fetch_object.is_empty())

    def test_is_source_valid(self):
        self.assertTrue(self.fetch_object.is_source_valid(self.source))
        self.assertTrue(self.fetch_object.is_source_valid(self.source2))

    def test_is_source_active(self):
        self.assertTrue(self.fetch_object.is_source_active(self.source))
        self.assertTrue(self.fetch_object.is_source_active(self.source2))

    def test_get_unknown_source(self):
        self.assertNotEqual(self.fetch_object.get_unknown_source(), 
        self.fetch_object.get_unknown_source())
        # prefix should be the same
        self.assertIn(self.fetch_object.unknown_source_prefix, 
        self.fetch_object.get_unknown_source())


    def test_read(self):
        # binary output is expected
        self.assertEqual(self.fetch_object.read(), b'')
        # check if everything from file is being fetched
        self.fetch_object.get_file().write(b'bytes')
        self.assertEqual(self.fetch_object.read(), b'bytes')
        # check if optional arguments passed to file.read()
        self.assertEqual(self.fetch_object.read(2), b'by')

    def test_fetch(self):
        output = self.fetch_object.fetch(self.source)
        # bytes output is expected
        self.assertIsInstance(output, bytes)
        self.assertGreater(len(output), 0)

    def test_fetch_to_file(self):
        with BytesIO() as f:
            self.fetch_object.fetch_to_file(self.source, f)
            self.assertGreater(f.tell(), 0)

    def test_request(self):
        self.fetch_object.request()
        fetch_file = self.fetch_object.get_file()
        self.assertGreater(fetch_file.tell(), 0)

    def test_clear(self):
        file = self.fetch_object.get_file()
        file.write(b"bytes")
        self.fetch_object.clear()
        self.assertEqual(file.tell(), 0)

