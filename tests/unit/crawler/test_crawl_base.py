import helper
# folders in src to path
# src_to_path() add folder in src to path
helper.src_to_path(__file__)

import unittest
from crawler.crawl_base import Crawl_Base
from crawler.text.text import Section


class TestText(unittest.TestCase):
    def setUp(self):
        self.source = "source of text"
        self.title = "title of resource"

    def test___init__(self):
        crawl_obj = Crawl_Base(self.source, self.title)
        self.assertEqual(crawl_obj.get_source(), self.source)
        self.assertEqual(crawl_obj.get_title(), self.title)
        self.assertEqual(crawl_obj.get_title(), self.title)

    def test_is_source_valid(self):
        crawl_obj = Crawl_Base(self.source, self.title)
        with self.assertRaises(NotImplementedError):
            crawl_obj.is_source_valid(self)

    def test_is_source_active(self):
        crawl_obj = Crawl_Base(self.source, self.title)
        with self.assertRaises(NotImplementedError):
            crawl_obj.is_source_active(self)

    def test_is_crawled(self):
        crawl_obj = Crawl_Base(self.source, self.title)
        self.assertFalse(crawl_obj.is_crawled())

    def test_crawl(self):
        crawl_obj = Crawl_Base(self.source, self.title)
        with self.assertRaises(NotImplementedError):
            crawl_obj.crawl(self)

    def test_request(self):
        crawl_obj = Crawl_Base(self.source, self.title)
        # check type error raised on wrong argumets
        with self.assertRaises(TypeError):
            crawl_obj.request("")
        with self.assertRaises(TypeError):
            crawl_obj.request(3, "")
        # NotImplementedError should be raised
        # most methods it relies on are not implemeted
        with self.assertRaises(NotImplementedError):
            crawl_obj.request()

if __name__ == '__main__':
    unittest.main()


