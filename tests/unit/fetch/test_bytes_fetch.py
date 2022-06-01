from io import BytesIO
import unittest

from naval.fetch.bytes_fetch import Bytes_Fetch
from .common_tests import Common_Tests


class Test_Bytes_Fetch(Common_Tests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = b"This is bytes string"
        cls.source2 = b"<p>This is html pragraph</p>"
        
        cls.fetch_object = Bytes_Fetch(cls.source)
        cls.fetch_object2 = Bytes_Fetch(cls.source2, content_type="html")

        cls.bytes_file = BytesIO()

    def test_is_source_valid(self) -> bool:
        # bytes are supported
        self.assertTrue(Bytes_Fetch.is_source_valid(self.source))
        # file object is not supported
        self.assertFalse(Bytes_Fetch.is_source_valid(self.bytes_file))
        # string are not supported
        self.assertFalse(Bytes_Fetch.is_source_valid(self.source.decode()))



if __name__ == '__main__':
    unittest.main()
