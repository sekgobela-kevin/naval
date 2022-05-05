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

    def __eq__(self):
        text_section = Text_Section(self.text1, (3,10))
        text_section2 = Text_Section(" ", (3,4))
        self.assertTrue(text_section == text_section)
        self.assertFalse(text_section == text_section2)
        self.assertTrue(text_section == self.text1)

    def test__hash__(self, /):
        text_section = Text_Section(self.text1, (3,10))
        text_section2 = Text_Section("", (3,10))
        self.assertNotEqual(hash(text_section), hash(text_section2))
        self.assertEqual(hash(text_section), hash(text_section))

if __name__ == '__main__':
    unittest.main()