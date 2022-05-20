import os
import unittest
from src.pynavy.crawler.crawler import *


class Test_Crawler_Functions(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "https://www.example"
        self.file_url = "https://www.example/file.pdf"
        self.local_file_path = __file__
        self.local_folder = os.path.join("path", "folder", "item")

    def test_create_start_end_indexes(self):
        # this test is same test method in utility/test_container.py
        self.assertEqual(create_start_end_indexes(10, 5), ((0,5), (5,10)))
        start_end_indexes = create_start_end_indexes(10, 2)
        self.assertEqual(start_end_indexes, ((0,2), (2,4), (4,6),(6, 8),(8, 10)))
        self.assertEqual(create_start_end_indexes(1,2), ((0,1),))
        self.assertEqual(create_start_end_indexes(0,1), ())

    def test_split_text(self):
        text = "0123456789"
        self.assertEqual(split_text(text, 5), ["01234", "56789"])
        self.assertEqual(split_text(text, 2), ["01","23","45","67","89"])
        self.assertEqual(split_text("", 2), [])

    def test_create_text_sections(self):
        text = "0123456789"
        section_objs = create_text_sections(text, 2)
        sections_texts = [section.get_text() for section in section_objs]
        self.assertEqual(sections_texts, ["01","23","45","67","89"])

    def test_sections_to_text(self):
        texts = ["01","23","45","67","89"]
        sections = [Text_Section(text, (0,1)) for text in texts]
        self.assertEqual(sections_to_text(sections), texts)

    def test_get_start_end_indexes(self):
        self.assertEqual(get_start_end_indexes(["01234", "56789"]), ((0,5), (5,10)))
        start_end_indexes = get_start_end_indexes(["01","23","45","67","89"])
        self.assertEqual(start_end_indexes, ((0,2), (2,4), (4,6),(6, 8),(8, 10)))
        self.assertEqual(get_start_end_indexes(["01234"]), ((0,5),))

if __name__ == '__main__':
    unittest.main()
