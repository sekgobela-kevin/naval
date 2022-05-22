from io import BytesIO
import os
import unittest
from pynavy.crawler.crawler import *
from pynavy.utility import directories


class Test_Text_Functions(unittest.TestCase):
    def setUp(self) -> None:
        self.text = "0123456789"

    def test_create_start_end_indexes(self):
        # this test is same test method in utility/test_container.py
        self.assertEqual(create_start_end_indexes(10, 5), ((0,5), (5,10)))
        start_end_indexes = create_start_end_indexes(10, 2)
        self.assertEqual(start_end_indexes, ((0,2), (2,4), (4,6),(6, 8),(8, 10)))
        self.assertEqual(create_start_end_indexes(1,2), ((0,1),))
        self.assertEqual(create_start_end_indexes(0,1), ())

    def test_split_text(self):
        self.assertEqual(split_text(self.text, 5), ["01234", "56789"])
        self.assertEqual(split_text(self.text, 2), ["01","23","45","67","89"])
        self.assertEqual(split_text("", 2), [])

    def test_create_text_sections(self):
        section_objs = create_text_sections(self.text, 2)
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


class Test_Download_Functions(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "https://www.example"
        self.url2 = "https://www.google.com"
        self.urls = [self.url, self.url2]
        self.folder_path = self.__class__.folder_path
        self.bytes_file = BytesIO()
        # remove downloaded files after each test
        directories.delete_folder_contents(self.folder_path)

    def tearDown(self):
        # this seems to be waste of time and bytes
        # is it worth it to close memory file here?
        self.bytes_file.close()

    @classmethod
    def setUpClass(cls):
        cls.folder_path = "downloads"
        directories.create_dir(cls.folder_path)

    @classmethod
    def tearDownClass(cls):
        directories.delete_dir(cls.folder_path)

    def test_download(self):
        file_path = os.path.join(self.folder_path, "file.txt")
        # download to file object
        download(self.url, self.bytes_file)
        self.assertGreater(self.bytes_file.tell(), 0)
        # download to file in disc
        download(self.url, file_path)
        # checks if file was created
        self.assertTrue(os.path.exists(file_path))
        # check if file is not empty
        self.assertFalse(directories.is_file_empty(file_path))


    def test_download_all(self):
        download_all(self.folder_path, self.urls)
        file_paths = directories.get_file_paths(self.folder_path)
        # 2 files should be downloaded
        self.assertEqual(len(file_paths), 2)
        for file_path in directories.get_file_paths(self.folder_path):
            # check if file is not empty
            self.assertFalse(directories.is_file_empty(file_path))


class Test_Extract_Functions(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = __file__
        self.file_object = open(self.file_path)
        self.file_path2 = "file.txt"
        self.file_object2 = open(self.file_path2, "w+")

    def tearDown(self):
        self.file_object.close()
        self.file_object2.close()
        try:
            os.unlink(self.file_path2)
        except FileNotFoundError:
            pass

    def test_extract_text(self):
        # test with file path
        self.assertGreater(len(extract_text(self.file_path)), 0)
        # test with file object
        self.assertGreater(len(extract_text(self.file_object)), 0)
        # test with empty file
        self.assertEqual(len(extract_text(self.file_path2)), 0)

    def test_extract_html(self):
        # not yet implemetened to text files
        # pdf and docx can be converted to html
        with self.assertRaises(NotImplementedError):
            extract_html(self.file_path)

    def test_extract_text_to_file(self):
        extract_text_to_file(self.file_path, self.file_path2)
        # checks if file was created
        self.assertTrue(os.path.exists(self.file_path2))
        self.assertFalse(directories.is_file_empty(self.file_path2))
        # using file objects instead of file paths
        extract_text_to_file(self.file_object, self.file_object2)
        # check if file object was written
        self.assertGreater(self.file_object2.tell(), 0)


    def test_extract_html_to_file(self):
        # not yet implemetened for text files
        # pdf and docx can be converted to html
        with self.assertRaises(NotImplementedError):
            # exceprion is raised by extract_html()
            extract_html_to_file(self.file_path, self.file_object2)


class Test_Register_Fetch(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = __file__
        self.url = "https://www.example"
        # remove all fetch classes
        Master_Fetch.fetch_classes.clear()

    def test_register_fetch_class(self):
        register_fetch_class(Web_Fetch)
        register_fetch_class(File_Fetch)
        # check if fetch classes are registered
        self.assertIn(Web_Fetch, Master_Fetch.fetch_classes)
        self.assertIn(File_Fetch, Master_Fetch.fetch_classes)


    def test_fetch_class_registered(self):
        self.assertFalse(fetch_class_registered(Web_Fetch))
        register_fetch_class(Web_Fetch)
        self.assertTrue(fetch_class_registered(Web_Fetch))

    def test_deregister_fetch_class(self):
        register_fetch_class(Web_Fetch)
        deregister_fetch_class(Web_Fetch)
        self.assertNotIn(Web_Fetch, Master_Fetch.fetch_classes)

    def test_deregister_fetch_classes(self):
        register_fetch_class(Web_Fetch)
        register_fetch_class(File_Fetch)
        # should deregister all fetch classes
        deregister_fetch_classes()
        self.assertEqual(len(Master_Fetch.fetch_classes), 0)
        register_fetch_class(Web_Fetch)
        register_fetch_class(File_Fetch)
        # should deregister Web_Fetch only
        deregister_fetch_classes([Web_Fetch])
        self.assertEqual(Master_Fetch.fetch_classes, {File_Fetch,})


    def test_get_registered_fetch_classes(self):
        # refererance to Master_Fetch.fetch_classes be returned
        self.assertIs(get_registered_fetch_classes(), 
        Master_Fetch.fetch_classes)
        get_registered_fetch_classes().add(File_Fetch)
        # changes should reflect to registered fetch classes
        self.assertEqual(Master_Fetch.fetch_classes, {File_Fetch,})


class Test_Register_Parse(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = __file__
        self.url = "https://www.example"
        # remove all parse classes
        Master_Parse.parse_classes.clear()

    def test_register_parse_class(self):
        register_parse_class(HTML_Parse)
        register_parse_class(PDF_Parse)
        # check if parse classes are registered
        self.assertIn(HTML_Parse, Master_Parse.parse_classes)
        self.assertIn(PDF_Parse, Master_Parse.parse_classes)


    def test_parse_class_registered(self):
        self.assertFalse(parse_class_registered(HTML_Parse))
        register_parse_class(HTML_Parse)
        self.assertTrue(parse_class_registered(HTML_Parse))

    def test_deregister_parse_class(self):
        register_parse_class(HTML_Parse)
        deregister_parse_class(HTML_Parse)
        self.assertNotIn(HTML_Parse, Master_Parse.parse_classes)

    def test_deregister_parse_classes(self):
        register_parse_class(HTML_Parse)
        register_parse_class(PDF_Parse)
        # should deregister all parse classes
        deregister_parse_classes()
        self.assertEqual(len(Master_Parse.parse_classes), 0)
        register_parse_class(HTML_Parse)
        register_parse_class(PDF_Parse)
        # should deregister HTML_Parse only
        deregister_parse_classes([HTML_Parse])
        self.assertEqual(Master_Parse.parse_classes, {PDF_Parse,})


    def test_get_registered_parse_classes(self):
        # refererance to Master_Parse.parse_classes be returned
        self.assertIs(get_registered_parse_classes(), 
        Master_Parse.parse_classes)
        get_registered_parse_classes().add(PDF_Parse)
        # changes should reflect to registered parse classes
        self.assertEqual(Master_Parse.parse_classes, {PDF_Parse,})

if __name__ == '__main__':
    unittest.main()
