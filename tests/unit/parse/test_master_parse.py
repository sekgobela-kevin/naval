import unittest
import os
from io import IOBase

from naval.fetch.fetch_base import Fetch_Base
from naval.fetch.file_fetch import File_Fetch

from naval.parse.parse_base import Parse_Base
from naval.parse.text_parse import Text_Parse
from naval.parse.pdf_parse import PDF_Parse
from naval.parse.master_parse import Master_Parse


class Test_Master_Parse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text_source = os.path.join("samples", "sample_file.txt")
        cls.invalid_source = os.path.join("samples", "sample_file.file")
        cls.pdf_source = os.path.join("samples", "sample_file.pdf")

        cls.text_fetch = File_Fetch(cls.text_source )
        cls.invalid_fetch = File_Fetch(cls.invalid_source)
        cls.pdf_fetch = File_Fetch(cls.pdf_source)

    def setUp(self):
        # dont remove this lines
        Master_Parse.parse_classes.clear()
        Master_Parse.parse_classes.add(Text_Parse)
        Master_Parse.parse_classes.add(PDF_Parse)

    def test_is_source_parsable(self):
        self.assertTrue(Master_Parse.is_source_parsable(self.text_source))
        self.assertFalse(Master_Parse.is_source_parsable(self.invalid_source))
        self.assertTrue(Master_Parse.is_source_parsable(self.pdf_source))

    def test_is_fetch_parsable(self):
        self.assertTrue(Master_Parse.is_fetch_parsable(self.text_fetch))
        self.assertFalse(Master_Parse.is_fetch_parsable(self.invalid_fetch))
        self.assertTrue(Master_Parse.is_fetch_parsable(self.pdf_fetch))

    def test_parse_class_exists(self):
        self.assertTrue(Master_Parse.parse_class_exists(self.text_fetch))
        self.assertFalse(Master_Parse.parse_class_exists(self.invalid_fetch))
        self.assertTrue(Master_Parse.parse_class_exists(self.pdf_fetch))


    def test_get_parse_class(self):
        parse_class = Master_Parse.get_parse_class(self.text_fetch)
        self.assertEqual(parse_class, Text_Parse)

    def test_get_parse_object(self):
        parse_obj = Master_Parse.get_parse_object(self.text_fetch)
        self.assertIsInstance(parse_obj, Text_Parse)

    def test_get_text(self):
        text = Master_Parse.get_text(self.text_fetch)
        self.assertEqual(type(text), str)
        self.assertGreater(len(text), 0)

    def test_get_html(self):
        html = Master_Parse.get_html(self.pdf_fetch)
        self.assertEqual(type(html), str)
        self.assertGreater(len(html), 0)

    def test_get_text_file(self):
        file_obj = Master_Parse.get_text_file(self.text_fetch)
        self.assertIsInstance(file_obj, IOBase)
        self.assertGreater(file_obj.tell(), 0)
        file_obj.close()

    def test_get_html_file(self):
        file_obj = Master_Parse.get_html_file(self.pdf_fetch)
        self.assertIsInstance(file_obj, IOBase)
        self.assertGreater(file_obj.tell(), 0)
        file_obj.close()

    def test_register_parse_class(self):
        # deregister existing parse classes
        Master_Parse.parse_classes.clear()
        Master_Parse.register_parse_class(Text_Parse)
        self.assertIn(Text_Parse, Master_Parse.parse_classes)
    
    def test_parse_class_registered(self):
        Master_Parse.parse_classes.remove(Text_Parse)
        self.assertFalse(Master_Parse.parse_class_registered(Text_Parse))
        self.assertTrue(Master_Parse.parse_class_registered(PDF_Parse))

    def test_deregister_parse_class(self):
        Master_Parse.deregister_parse_class(Text_Parse)
        self.assertNotIn(Text_Parse, Master_Parse.parse_classes)
        self.assertIn(PDF_Parse, Master_Parse.parse_classes)

    def test_deregister_parse_classes(self):
        Master_Parse.deregister_parse_classes()
        self.assertEqual(len(Master_Parse.parse_classes), 0)


if __name__ == '__main__':
    unittest.main()
