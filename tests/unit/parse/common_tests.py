from io import BytesIO, IOBase
from naval.fetch.fetch_base import Fetch_Base
from naval.parse.parse_base import Parse_Base

class Common_Tests(object):
    @classmethod
    def setUpClass(cls):
        cls.source: str
        cls.source2: str

        cls.fetch_obj: Fetch_Base
        cls.fetch_obj2: Fetch_Base

        cls.parse_obj: Parse_Base
        cls.parse_obj2: Parse_Base

    def test_get_doc(self):
        doc_obj = self.parse_obj.get_doc()
        self.assertIsInstance(doc_obj, object)

    def test_is_file_empty(self):
        file_obj = BytesIO()
        self.assertTrue(self.parse_obj.is_file_empty(file_obj))
        file_obj.write(b"something")
        self.assertFalse(self.parse_obj.is_file_empty(file_obj))

    def test_text_to_file(self):
        self.parse_obj.text_to_file()
        text_file = self.parse_obj.get_text_file()
        self.assertFalse(self.parse_obj.is_file_empty(text_file))

    def test_html_to_file(self):
        self.parse_obj.html_to_file()
        html_file = self.parse_obj.get_html_file()
        self.assertFalse(self.parse_obj.is_file_empty(html_file))

    def test_get_text_file(self):
        file_obj = self.parse_obj.get_text_file()
        self.assertIsInstance(file_obj, IOBase)

    def test_get_html_file(self):
        file_obj = self.parse_obj.get_html_file()
        self.assertIsInstance(file_obj, IOBase)

    def test_get_file_copy(self):
        file_obj = BytesIO()
        file_copy = self.parse_obj.get_file_copy(file_obj)
        file_copy.write("something")
        self.assertEqual(file_obj.tell(), 0)
        self.assertGreater(file_copy.tell(), 0)
        file_copy.close()

    def test_get_text_file_copy(self):
        file_obj = self.parse_obj.get_text_file_copy()
        self.assertIsInstance(file_obj, IOBase)
        file_obj.close()

    def test_get_html_file_copy(self):
        file_obj = self.parse_obj.get_html_file_copy()
        self.assertIsInstance(file_obj, IOBase)
        file_obj.close()
    
    def test_get_fetch(self):
        fetch_obj = self.parse_obj.get_fetch()
        self.assertIsInstance(fetch_obj, Fetch_Base)
    
    def test_get_title(self):
        self.assertIsInstance(self.parse_obj.get_title(), (str, type(None)))
    
    def test_get_text(self):
        text = self.parse_obj.get_text()
        # assertIsInstance would print log text on failure
        self.assertEqual(type(text), str)
        self.assertGreater(len(text), 0)

    def test_get_html(self):
        html = self.parse_obj.get_html()
        # assertIsInstance would print log text on failure
        self.assertEqual(type(html), str)
        self.assertGreater(len(html), 0)

    def test_get_container(self):
        pass

    def text_to_container(self):
        pass

    def html_to_container(self):
        pass