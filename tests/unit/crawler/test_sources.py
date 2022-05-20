import os
import unittest
from src.pynavy.crawler.sources import *


class Test_Sources_Methods(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "https://www.example"
        self.file_url = "https://www.example/file.pdf"
        self.local_file_path = __file__
        self.local_folder = os.path.join("path", "folder", "item")

    def test_is_url(self):
        self.assertTrue(is_url(self.url))
        self.assertTrue(is_url(self.file_url))
        self.assertFalse(is_url(self.local_file_path))

    def test_is_local_file(self):
        self.assertTrue(is_local_file(self.local_file_path))
        self.assertFalse(is_local_file(self.file_url))

        self.assertFalse(is_web_file(self.url))
        self.assertTrue(is_web_file(self.file_url))
        self.assertFalse(is_web_file(self.local_file_path))     

    def test_is_file(self):
        self.assertFalse(is_file(self.url))
        self.assertTrue(is_file(self.file_url))
        self.assertTrue(is_file(self.local_file_path))     


    def test_is_pdf_file(self):
        self.assertTrue(is_pdf_file("file.pdf"))
        self.assertFalse(is_pdf_file("file.csv"))

    def test_is_docx_file(self):
        self.assertTrue(is_docx_file("file.docx"))
        self.assertFalse(is_docx_file("file.csv"))

    def test_is_pptx_file(self):
        self.assertTrue(is_pptx_file("file.pptx"))
        self.assertFalse(is_pptx_file("file.csv"))

    def test_is_html_file(self):
        self.assertTrue(is_html_file("file.html"))
        self.assertTrue(is_html_file("file.htm"))
        self.assertFalse(is_html_file("file.csv"))

    def test_is_text_file(self):
        self.assertTrue(is_text_file("file.html"))
        self.assertTrue(is_text_file("file.txt"))
        self.assertFalse(is_text_file("file.pdf"))


if __name__ == '__main__':
    unittest.main()
