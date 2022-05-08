from io import FileIO, IOBase
import unittest
import tempfile
from src.pynavy.crawler.parse.parse_base import Parse_Base
from src.pynavy.crawler.fetch.master_fetch import Master_Fetch


class Test_Fetch_Base(unittest.TestCase):
    def setUp(self):
        self.source = __file__
        self.file_fetch = Master_Fetch.get_fetch_object(self.source)
        self.parse_obj = Parse_Base(self.file_fetch)

    def test_to_text(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.to_text()

    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.to_html()

    def test_to_container(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.to_container()


if __name__ == '__main__':
    unittest.main()
