from io import BytesIO
import unittest

from naval.fetch.string_fetch import String_Fetch
from .common_tests import Common_Tests


class Test_String_Fetch(Common_Tests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = "This is text string"
        cls.source2 = "<p>This is html paragraph</p>"
        
        cls.fetch_object = String_Fetch(cls.source)
        cls.fetch_object2 = String_Fetch(cls.source2, content_type="html")

        cls.bytes_file = BytesIO()

    def test_is_source_valid(self) -> bool:
        self.assertTrue(self.fetch_object.is_source_valid(self.source))
        # file object is not supported
        self.assertFalse(self.fetch_object.is_source_valid(self.bytes_file))
        # bytes not supported
        self.assertFalse(self.fetch_object.is_source_valid(self.source.encode()))

    def test_get_content_type(self):
        self.assertEqual(self.fetch_object.get_content_type(), None)
        self.assertEqual(self.fetch_object2.get_content_type(), 'text/html')


if __name__ == '__main__':
    unittest.main()
