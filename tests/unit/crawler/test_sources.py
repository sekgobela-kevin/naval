import os
import unittest
from src.pynavy.crawler.sources import *
from src.pynavy.utility import directories


class Test_Sources_Methods(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "https://www.example"
        self.file_url = "https://www.example/file.pdf"
        self.local_file_path = __file__
        self.local_folder = os.path.join("path", "folder", "item")
        self.folder_path = "folder"
        directories.create_dir(self.folder_path)

    def tearDown(self):
        directories.delete_dir(self.folder_path)
        
    def test_is_url(self):
        self.assertTrue(is_url(self.url))
        self.assertTrue(is_url(self.file_url))
        self.assertFalse(is_url(self.local_file_path))

    def test_get_url_path(self):
        self.assertEqual(get_url_path(self.file_url), "/file.pdf")

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

    def test_is_plain_text_file(self):
        self.assertFalse(is_plain_text_file("file.html"))
        self.assertTrue(is_plain_text_file("file.txt"))

    def test_get_urls_from_html(self):
        html = '''<div>
        <a href='example.com'></a>
        <a href='google.com'></a>
        </div>'''
        self.assertEqual(get_urls_from_html(html), {"example.com",
        "google.com"})

    def test_get_urls_from_text(self):
        text = '''https://example.com/file.txt
        http://example.com/
        /folder/file.txt'''
        self.assertEqual(get_urls_from_text(text), {
            "https://example.com/file.txt",
            "http://example.com/"
        })

    def test_get_file_paths(self):
        file_path = os.path.join(self.folder_path, "file.txt")
        file2_path = os.path.join(self.folder_path, "file.htm")
        # creates files
        directories.create_file(file_path)
        directories.create_file(file2_path)
        # checks if path to files is returned
        self.assertCountEqual(get_file_paths(self.folder_path), {
            file_path, file2_path
        })


if __name__ == '__main__':
    unittest.main()
