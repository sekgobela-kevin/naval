import unittest
from src.pynavy.crawler.crawl_base import Crawl_Base


class Test_Crawl_Base(unittest.TestCase):
    def setUp(self):
        self.source = __file__
        self.title = "title of resource"

    def test___init__(self):
        crawl_obj = Crawl_Base(self.source)
        self.assertEqual(crawl_obj.get_source(), self.source)
        self.assertEqual(crawl_obj.get_title(), "")

    def test_is_crawled(self):
        crawl_obj = Crawl_Base(self.source)
        self.assertFalse(crawl_obj.is_crawled())

    def test_parse(self):
        crawl_obj = Crawl_Base(self.source)
        with self.assertRaises(NotImplementedError):
            crawl_obj.parse(self)

    def test_request(self):
        crawl_obj = Crawl_Base(self.source)
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


