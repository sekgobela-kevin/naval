from io import BytesIO, FileIO, IOBase
import unittest
import os

from naval.fetch.fetch_base import Fetch_Base
from naval.parse.docx_parse import DOCX_Parse
from naval.parse.docx_parse import Parse_Base
from naval.fetch.master_fetch import Master_Fetch

from .common_tests import Common_Tests
from docx.parts.document import Document

class Test_DOCX_Parse(unittest.TestCase, Common_Tests):
    @classmethod
    def setUpClass(cls):
        cls.source = os.path.join("samples", "sample_file.docx")
        cls.source2 = os.path.join("samples", "sample_file.file")

        cls.fetch_obj = Master_Fetch.get_fetch_object(cls.source)
        cls.fetch_obj2 = Master_Fetch.get_fetch_object(cls.source2)

        # mainly use cls.parse_obj other than cls.parse_obj
        cls.parse_obj = DOCX_Parse(cls.fetch_obj)
        cls.parse_obj2 = Parse_Base(cls.fetch_obj2)

    def test_get_doc(self):
        doc_obj = self.parse_obj.get_doc()
        self.assertIsInstance(doc_obj, Document)


if __name__ == '__main__':
    unittest.main()
