import unittest
from src.pynavy.crawler.fetch.fetch import Fetch
from src.pynavy.crawler.parse.parse import Parse
from src.pynavy.crawler.crawl_base import Crawl_Base


class Test_Crawl_Base(unittest.TestCase):
    def setUp(self):
        self.source = __file__
        self.fetch_obj = Fetch(self.source)
        self.crawl_obj = Crawl_Base(self.source)

    def test___init__(self):
        self.crawl_obj = Crawl_Base(self.source)
        self.assertEqual(self.crawl_obj.get_source(), self.source)
        self.assertEqual(self.crawl_obj.get_title(), "")

    def test_get_fetch(self):
        fetch_obj = self.crawl_obj.get_fetch(self.source)
        self.assertIsInstance(fetch_obj, Fetch)

    def test_get_parse(self):
        parse_obj = self.crawl_obj.get_parse(self.fetch_obj)
        self.assertIsInstance(parse_obj, Parse)

    def test_crawl(self):
        self.crawl_obj.crawl(self.source)
        # crawl object should is not be empty
        self.assertGreater(len(self.crawl_obj), 0)

if __name__ == '__main__':
    unittest.main()


