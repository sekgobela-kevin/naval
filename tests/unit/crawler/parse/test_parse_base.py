from io import FileIO, IOBase
import unittest
import tempfile
from pynavy.crawler.parse.parse_base import Parse_Base
from pynavy.crawler.fetch.master_fetch import Master_Fetch


class Test_Fetch_Base(unittest.TestCase):
    def setUp(self):
        self.source = __file__
        self.file_fetch = Master_Fetch.get_fetch_object(self.source)
        self.parse_obj = Parse_Base(self.file_fetch)



if __name__ == '__main__':
    unittest.main()
