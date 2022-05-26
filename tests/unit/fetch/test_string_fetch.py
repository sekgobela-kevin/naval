from io import BytesIO
import unittest
from naval.fetch.string_fetch import String_Fetch


class Test_String_Fetch(unittest.TestCase):
    def setUp(self):
        self.text = "This is text string"
        self.html = "<p>This is html pragraph</p>"
        self.fetch_obj = String_Fetch(self.text)
        self.fetch_obj2 = String_Fetch(self.html, content_type="html")
        self.bytes_file = BytesIO()

    def tearDown(self):
        self.fetch_obj.close()
        self.fetch_obj2.close()

    def test_is_source_valid(self) -> bool:
        self.assertTrue(String_Fetch.is_source_valid(self.text))
        # file object is not supported
        self.assertFalse(String_Fetch.is_source_valid(self.bytes_file))
        # bytes not supported
        self.assertFalse(String_Fetch.is_source_valid(self.text.encode()))

    def test_get_content_type(self):
        self.assertEqual(self.fetch_obj.get_content_type(), None)
        self.assertEqual(self.fetch_obj2.get_content_type(), 'text/html')

    def test_read(self):
        # if this succeeds then everything is doing well
        # the other tests are covered by test_file_fetch.py
        self.assertEqual(self.fetch_obj.read().decode(), self.text)


if __name__ == '__main__':
    unittest.main()
