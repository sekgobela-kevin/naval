import unittest
from src.pynavy.crawler.text.section import Section


class TestSection(unittest.TestCase):
    def setUp(self):
        self.text1 = "Programming is improves your brain"
        self.text2 = "Life without money is a hell"

    def test_size(self):
        section_obj = Section(self.text1, [3,10])
        self.assertEqual(section_obj.size(), len(self.text1))
    
    def test_get_text(self):
        section_obj = Section(self.text1, [3,10])
        self.assertEqual(section_obj.get_text(), self.text1)

    def test_get_metadata(self):
        section_obj = Section(self.text1, [3,10], {"index": 3})
        self.assertEqual(section_obj.get_metadata(), {"index": 3})
    
    def test_set_metadata(self):
        section_obj = Section(self.text1, [3,10])
        section_obj.set_metadata({"index": 0})
        self.assertEqual(section_obj.get_metadata(), {"index": 0})
        with self.assertRaises(ValueError):
            section_obj.set_metadata(10)

    def test_get_data(self):
        section_obj = Section(self.text1, [3,10], {"index": 2})
        self.assertEqual(section_obj.get_data("index"), 2)

    def test_add_data(self):
        section_obj = Section(self.text1, [3,10])
        section_obj.add_data("index", 2)
        self.assertEqual(section_obj.get_data("index"), 2)
        with self.assertRaises(KeyError):
            section_obj.get_data("type")

    def test_data_exists(self):
        section_obj = Section(self.text1, [3,10], {"index": 2})
        self.assertTrue(section_obj.data_exists("index"))
        self.assertFalse(section_obj.data_exists("type"))

    def test_remove_data(self):
        section_obj = Section(self.text1, [3,10])
        section_obj.add_data("index", 2)
        self.assertTrue(section_obj.data_exists("index"))
        section_obj.remove_data("index")
        self.assertFalse(section_obj.data_exists("index"))

    def test_get_metadata_size(self):
        section_obj = Section(self.text1, [3,10], {"index": 2, "length": 4000})
        self.assertEqual(section_obj.get_metadata_size(), 2)

    
    def test__contains__(self):
        section_obj = Section(self.text1, [3,10])
        self.assertTrue("Programming" in section_obj)
        self.assertFalse("computers" in section_obj)

    def test__iter__(self):
        section_obj = Section("123", [3,10])
        self.assertEqual(list(iter(section_obj)), list("123"))

    def test__next__(self):
        section_obj = Section(self.text1, [3,10])
        self.assertEqual(next(section_obj), "P")
        self.assertEqual(next(section_obj), "r")
        with self.assertRaises(StopIteration):
            while True:
                next(section_obj)

    def test__len__(self, /):
        section_obj = Section(self.text1, [3,10])
        self.assertEqual(len(section_obj), len(self.text1))

    def __eq__(self):
        section_obj = Section(self.text1, [3,10])
        section_obj_ = Section(self.text1, [3,10])
        section_obj2 = Section(self.text2, [3,10])
        section_obj3 = Section(self.text1, [3,6])
        self.assertTrue(section_obj == section_obj)
        self.assertTrue(section_obj == section_obj_)
        self.assertFalse(section_obj == section_obj2)
        self.assertFalse(section_obj == section_obj3)
        with self.assertRaises(NotImplemented):
            section_obj == ""

    def __ne__(self):
        section_obj = Section(self.text1, [3,10])
        section_obj_ = Section(self.text1, [3,10])
        section_obj2 = Section(self.text2, [3,10])
        section_obj3 = Section(self.text1, [3,6])
        self.assertTrue(section_obj != section_obj)
        self.assertFalse(section_obj != section_obj_)
        self.assertTrue(section_obj != section_obj2)
        self.assertTrue(section_obj !=section_obj3)
        with self.assertRaises(NotImplemented):
            section_obj != ""

    def test__bool__(self, /):
        section_obj = Section(self.text1, [3,10])
        section_obj2 = Section("", [3,10])
        self.assertTrue(bool(section_obj))
        self.assertFalse(bool(section_obj2))

    def test__getitem__(self, /):
        section_obj = Section(self.text1, [3,10])
        self.assertEqual(section_obj[0], self.text1[0])
        self.assertEqual(section_obj[0:8], self.text1[0:8])
        self.assertEqual(section_obj[0:8:2], self.text1[0:8:2])

    def test__hash__(self, /):
        section_obj = Section(self.text1, [3,10])
        section_obj2 = Section("", [3,10])
        self.assertNotEqual(hash(section_obj), hash(section_obj2))
        self.assertEqual(hash(section_obj), hash(section_obj))

if __name__ == '__main__':
    unittest.main()