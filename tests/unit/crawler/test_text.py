import helper
# folders in src to path
# src_to_path() add folder in src to path
helper.src_to_path(__file__)

import unittest
from crawler.text.text import Text
from crawler.text.text import Section

class TestText(unittest.TestCase):
    def setUp(self):
        self.text1 = "0123456789"
        self.text2 = "Life without money is a hell"
        self.section_obj1 = Section(self.text1, (4,5))
        self.section_obj2 = Section(self.text2, (4,5))

    def test_size(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.size(), 0)

    def test_get_title(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.get_source(), "source")

    def test_get_title(self):
        text_obj = Text("source", "title")
        self.assertEqual(text_obj.get_title(), "title")

    def test_get_start_end_indexes(self):
        text_obj = Text("source", "title")
        start_end_indexes = text_obj.get_start_end_indexes(len(self.text1), 5)
        self.assertEqual(start_end_indexes, [(0,5), (5,10)])
        start_end_indexes = text_obj.get_start_end_indexes(len(self.text1), 2)
        self.assertEqual(start_end_indexes, [(0,2), (2,4), (4,6),(6, 8), (8, 10)])
        start_end_indexes = text_obj.get_start_end_indexes(len(self.text1)+1, 2)
        self.assertEqual(start_end_indexes, [(0,2), (2,4), (4,6),(6, 8), 
            (8, 10), (10, 11)]
        )
        with self.assertRaises(Exception):
            text_obj.get_start_end_indexes(len(self.text1), len(self.text1)+1)

    def test_create_sections(self):
        text_obj = Text("source", "title")
        sections = text_obj.create_sections(self.text1, 2)
        start_end_indexes = [(0,2), (2,4), (4,6),(6, 8), (8, 10)]
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
        section_obj = Section(self.text1, (4,6))
        self.assertEqual(text_obj.size(), 0)
        text_obj.add_section(section_obj)
        self.assertEqual(text_obj.size(), 1)

    def test_get_section(self):
        text_obj = Text("source", "title")
        self.assertEqual(len(text_obj.get_sections()), 0)
        text_obj.add_section(self.section_obj1)
        self.assertEqual(len(text_obj.get_sections()), 1)

    
    def test_section_exists(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        self.assertTrue(text_obj.section_exists(lambda x: x.get_text() == self.text1))
        self.assertFalse(text_obj.section_exists(lambda x: x.get_text() == self.text2))

    def test_filter_sections(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        filtered = text_obj.filter_sections(lambda x: x.get_text() == self.text2)
        self.assertEqual(len(filtered), 1)
        filtered = text_obj.filter_sections(lambda x: x.get_text() == "")
        self.assertEqual(len(filtered), 0)
        filtered = text_obj.filter_sections(lambda x: True)
        self.assertEqual(len(filtered), 2)

    def test_get_sections(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        sections = text_obj.get_sections()
        self.assertEqual(len(sections), 2)

    def test_remove_section(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        self.assertEqual(text_obj.size(), 2)
        text_obj.section_exists(lambda x: x.get_text() == self.text1)
        text_obj.remove_section(lambda x: x.get_text() == self.text1)
        self.assertEqual(text_obj.size(), 1)
        with self.assertRaises(Exception):
            # does not exists
            text_obj.remove_section(lambda x: x.get_text() == "")

    def test_clear(self):
        text_obj = Text("source", "title", metadata={"keywords": ["john"],
            "size_chars":30000})
        text_obj.add_section(self.section_obj1)
        self.assertEqual(text_obj.get_metadata_size(), 2)
        self.assertEqual(text_obj.size(), 1)
        text_obj.clear()
        self.assertEqual(text_obj.get_metadata_size(), 0)
        self.assertEqual(text_obj.size(), 0)

    def test_get_text(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        self.assertEqual(text_obj.get_text(), self.text1+self.text2)



    def test__contains__(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        self.assertTrue(self.section_obj1 in text_obj)
        self.assertFalse(self.section_obj2 in text_obj)

    def test__iter__(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        self.assertEqual(len(list(iter(text_obj))), 1)

    def test__next__(self):
        text_obj = Text("source", "title")
        text_obj.add_section(self.section_obj1)
        text_obj.add_section(self.section_obj2)
        self.assertEqual(next(text_obj), self.section_obj1)
        self.assertEqual(next(text_obj), self.section_obj2)
        with self.assertRaises(StopIteration):
            while True:
                next(text_obj)

    def test__len__(self, /):
        text_obj = Text("source", "title")
        self.assertEqual(len(text_obj), 0)
        text_obj.add_section(self.section_obj1)
        self.assertEqual(len(text_obj), 1)

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
        text_obj2 = Text("source", "title_")
        text_obj_ = Text("", "")
        text_obj__ = Text("", "")
        self.assertEqual(hash(text_obj), hash(text_obj))
        self.assertNotEqual(hash(text_obj), hash(text_obj2))
        self.assertNotEqual(hash(text_obj_), hash(text_obj__))

if __name__ == '__main__':
    unittest.main()

