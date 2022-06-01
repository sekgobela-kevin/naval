import unittest

from naval.fetch.web_fetch import Web_Fetch
from .common_tests import Common_Tests


class Test_Web_Fetch(Common_Tests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = "https://www.google.com"
        cls.source2 = "https://www.example.com"

        cls.fetch_object = Web_Fetch(cls.source)
        cls.fetch_object2 = Web_Fetch(cls.source2)

    def test_is_source_valid(self):
        # both should be valid, they are valid urls
        self.assertTrue(self.fetch_object.is_source_valid(self.source))
        # both should be invalid, they are not urls
        self.assertFalse(self.fetch_object.is_source_valid(__file__))
        self.assertFalse(self.fetch_object.is_source_valid("path to file"))

    def test_is_source_active(self):
        pass

    # def test_is_source_active(self):
    #     # the two are valid and active
    #     self.assertTrue(Web_Fetch.is_source_active(self.url))
    #     self.assertTrue(Web_Fetch.is_source_active(self.url2))
    #     # the two are valid but not active
    #     self.assertFalse(Web_Fetch.is_source_active(self.url3))
    #     self.assertFalse(Web_Fetch.is_source_active(self.url4))
    #     with self.assertRaises(TypeError):
    #         # url should only be string
    #         Web_Fetch.is_source_active(44)   

