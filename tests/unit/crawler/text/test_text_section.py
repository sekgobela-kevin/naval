import unittest
from src.pynavy.crawler.text.text_section import Text_Section


class TestTextSection(unittest.TestCase):
    def setUp(self):
        self.text1 = "Programming is improves your brain"
        self.text2 = "Life without money is a hell"

    def test_size(self):
        text_section = Text_Section(self.text1, (3,10))
        self.assertEqual(text_section.size(), len(self.text1))
    
    def test_get_text(self):
        text_section = Text_Section(self.text1, (3,10))
        self.assertEqual(text_section.get_text(), self.text1)
    
    def test__contains__(self):
        text_section = Text_Section(self.text1, (3,10))
        self.assertTrue("Programming" in text_section)
        self.assertFalse("computers" in text_section)

    def test__iter__(self):
        text_section = Text_Section("123", (3,10))
        self.assertEqual(list(iter(text_section)), list("123"))

    def test__next__(self):
        text_section = Text_Section(self.text1, (3,10))
        self.assertEqual(next(text_section), "P")
        self.assertEqual(next(text_section), "r")
        with self.assertRaises(StopIteration):
            while True:
                next(text_section)

    def test__len__(self, /):
        text_section = Text_Section(self.text1, (3,10))
        self.assertEqual(len(text_section), len(self.text1))

    def test_key(self):
        text_section = Text_Section(self.text1, (3,10))
        text_section2 = Text_Section(self.text2, (3,10))
        self.assertEqual(text_section._key(), text_section._key())
        self.assertNotEqual(text_section._key(), text_section2._key())
        self.assertEqual(text_section._key(), hash(text_section.get_text()))

if __name__ == '__main__':
    unittest.main()