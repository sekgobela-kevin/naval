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

    def test_get_title(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.get_source(), "source")

    def test_get_title(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.get_title(), "title")

    def test_create_start_indexes(self):
        text_obj = Text("source", "title")
        start_indexes = text_obj.create_start_indexes(len(self.text1), 5)
        self.assertEqual(start_indexes, (0,5))
        start_indexes = text_obj.create_start_indexes(len(self.text1), 2)
        self.assertEqual(start_indexes, (0, 2, 4, 6, 8))
        start_indexes = text_obj.create_start_indexes(1, 2)
        self.assertEqual(start_indexes, (0,))
        start_indexes = text_obj.create_start_indexes(0, 2)
        self.assertEqual(start_indexes, ())

    def test_create_end_indexes(self):
        text_obj = Text("source", "title")
        end_indexes = text_obj.create_end_indexes(len(self.text1), 5)
        self.assertEqual(end_indexes, (5,10))
        end_indexes = text_obj.create_end_indexes(len(self.text1), 2)
        self.assertEqual(end_indexes, (2, 4, 6, 8, 10))
        end_indexes = text_obj.create_end_indexes(1, 2)
        self.assertEqual(end_indexes, (1,))
        end_indexes = text_obj.create_end_indexes(0, 2)
        self.assertEqual(end_indexes, ())

    def test_create_start_end_indexes(self):
        text_obj = Text("source", "title")
        start_end_indexes = text_obj.create_start_end_indexes(len(self.text1), 5)
        self.assertEqual(start_end_indexes, ((0,5), (5,10)))
        start_end_indexes = text_obj.create_start_end_indexes(len(self.text1), 2)
        self.assertEqual(start_end_indexes, ((0,2), (2,4), (4,6),(6, 8), (8, 10)))
        start_end_indexes = text_obj.create_start_end_indexes(len(self.text1)+1, 2)
        self.assertEqual(start_end_indexes, ((0,2), (2,4), (4,6),(6, 8), 
            (8, 10), (10, 11))
        )
        start_end_indexes = text_obj.create_start_end_indexes(1, 2)
        self.assertEqual(start_end_indexes, ((0,1),))
        start_end_indexes = text_obj.create_start_end_indexes(0, 2)
        self.assertEqual(start_end_indexes, ())

    def test_create_sections(self):
        text_obj = Text("source", "title")
        sections = text_obj.create_sections(self.text1, 2)
        start_end_indexes = ((0,2), (2,4), (4,6),(6, 8), (8, 10))
        self.assertEqual(len(sections), len(start_end_indexes))
        for i in range(len(sections)):
            start, end = start_end_indexes[i]
            section = sections[i]
            self.assertEqual(section.get_text(), self.text1[start:end])

    def test_create_section(self):
        text_obj = Text("source", "title")
        section_obj = text_obj.create_section(self.text1, (4, 8))
        self.assertEqual(section_obj.get_text(), self.text1[4:8])

    def test_add_section(self):
        text_obj = Text("source", "title")
        section_obj = Text_Section(self.text1, (4,6))
        self.assertEqual(text_obj.size(), 0)
        text_obj.add_section(section_obj)
        self.assertEqual(text_obj.size(), 1)

    def test_get_text(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        self.assertEqual(text_obj.get_text(), self.text1+self.text2)

    def __eq__(self):
        text_obj = Text("source", "title")
        text_obj2 = Text("source_", "title")
        self.assertTrue(text_obj == text_obj)
        self.assertFalse(text_obj == text_obj2)
        with self.assertRaises(NotImplemented):
            text_obj == ""

    def __ne__(self):
        text_obj = Text("source", "title")
        text_obj2 = Text("source_", "title")
        self.assertFalse(text_obj != text_obj)
        self.assertTrue(text_obj != text_obj2)
        with self.assertRaises(NotImplemented):
            text_obj != ""

    def test__bool__(self, /):
        text_obj = Text("source", "title")
        self.assertFalse(bool(text_obj))
        text_obj.add_section(self.section_obj1)
        self.assertTrue(bool(text_obj))

    def test__getitem__(self, /):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        self.assertEqual(text_obj[0], self.section_obj1)
        self.assertEqual(text_obj[1], self.section_obj2)

    def test__hash__(self, /):
        text_obj = Text("source", "title")
        text_obj2 = Text("source2", "title")
        self.assertEqual(hash(text_obj), hash(text_obj))
        self.assertNotEqual(hash(text_obj), hash(text_obj2))

if __name__ == '__main__':
    unittest.main()
