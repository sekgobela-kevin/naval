from io import BytesIO, FileIO, IOBase
import unittest
import os

from naval.fetch.fetch_base import Fetch_Base
from naval.parse.html_parse import HTML_Parse
from naval.parse.parse_base import Parse_Base
from naval.fetch.master_fetch import Master_Fetch

from .common_tests import Common_Tests


class Test_HTML_Parse(unittest.TestCase, Common_Tests):
    @classmethod
    def setUpClass(cls):
        cls.source = os.path.join("samples", "sample_file.html")
        cls.source2 = os.path.join("samples", "sample_file.file")

        cls.fetch_obj = Master_Fetch.get_fetch_object(cls.source)
        cls.fetch_obj2 = Master_Fetch.get_fetch_object(cls.source2)

        # mainly use cls.parse_obj other than cls.parse_obj
        cls.parse_obj = HTML_Parse(cls.fetch_obj)
        cls.parse_obj2 = Parse_Base(cls.fetch_obj2)


if __name__ == '__main__':
    unittest.main()
