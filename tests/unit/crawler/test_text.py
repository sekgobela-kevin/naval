import unittest
from src.pynavy.crawler.text.text import Text
from src.pynavy.crawler.text.text_section import Text_Section

class TestText(unittest.TestCase):
    def setUp(self):
        self.text1 = "0123456789"
        self.text2 = "Life without money is a hell"
        self.section_obj1 = Text_Section(self.text1, (0,4))
        self.section_obj2 = Text_Section(self.text2, (0,4))

    def test_size(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.size(), 0)

    def test_get_source(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.get_source(), "source")

    def test_get_title(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.get_title(), "title")

    def test_get_text(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        self.assertEqual(text_obj.get_text(), self.text1+self.text2)

    def test_key(self):
        text_obj = Text("source", "title")
        text_obj2 = Text("source_", "title")
        self.assertEqual(text_obj._key(), text_obj._key())
        self.assertNotEqual(text_obj._key(), text_obj2._key())
        self.assertEqual(text_obj._key(), hash(text_obj.get_source()))

if __name__ == '__main__':
    unittest.main()
