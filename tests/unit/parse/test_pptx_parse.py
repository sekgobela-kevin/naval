from io import BytesIO, FileIO, IOBase
import unittest
import os

from naval.fetch.fetch_base import Fetch_Base
from naval.parse.pptx_parse import PPTX_Parse
from naval.parse.pptx_parse import Parse_Base
from naval.fetch.master_fetch import Master_Fetch

from .common_tests import Common_Tests
from pptx.presentation import Presentation


class Test_PPTX_Parse(unittest.TestCase, Common_Tests):
    @classmethod
    def setUpClass(cls):
        cls.source = os.path.join("samples", "sample_file.pptx")
        cls.source2 = os.path.join("samples", "sample_file.file")

        cls.fetch_obj = Master_Fetch.get_fetch_object(cls.source)
        cls.fetch_obj2 = Master_Fetch.get_fetch_object(cls.source2)

        # mainly use cls.parse_obj other than cls.parse_obj
        cls.parse_obj = PPTX_Parse(cls.fetch_obj)
        cls.parse_obj2 = Parse_Base(cls.fetch_obj2)

    def test_get_doc(self):
        doc_obj = self.parse_obj.get_doc()
        self.assertIsInstance(doc_obj, Presentation)

    def test_html_to_file(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.html_to_file()

    def test_get_html(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.get_html()
if __name__ == '__main__':
    unittest.main()
