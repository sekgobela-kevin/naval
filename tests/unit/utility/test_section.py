import unittest
from pynavy.utility.section import Section


class TestSection(unittest.TestCase):
    def setUp(self):
        self.text1 = "Programming is improves your brain"
        self.text2 = "Life without money is a hell"

    def test_size(self):
        section_obj = Section(self.text1)
        self.assertEqual(section_obj.size(), len(self.text1))

    def test_index(self):
        section_obj = Section(self.text1, (0,5))
        self.assertEqual(section_obj.get_index(), (0, 5))

    def test_get_elements(self):
        section_obj = Section(self.text1)
        self.assertEqual(section_obj.get_elements(), self.text1)
    
    def test__contains__(self):
        section_obj = Section(self.text1)
        self.assertTrue("Programming" in section_obj)
        self.assertFalse("computers" in section_obj)

    def test__iter__(self):
        section_obj = Section("123")
        self.assertEqual(list(iter(section_obj)), list("123"))

    def test__next__(self):
        section_obj = Section(self.text1)
        self.assertEqual(next(section_obj), "P")
        self.assertEqual(next(section_obj), "r")
        with self.assertRaises(StopIteration):
            while True:
                next(section_obj)

    def test__len__(self, /):
        section_obj = Section(self.text1)
        self.assertEqual(len(section_obj), len(self.text1))


    def test__bool__(self, /):
        section_obj = Section(self.text1)
        section_obj2 = Section("")
        self.assertTrue(bool(section_obj))
        self.assertFalse(bool(section_obj2))

    def test__getitem__(self, /):
        section_obj = Section(self.text1)
        self.assertEqual(section_obj[0], self.text1[0])
        self.assertEqual(section_obj[0:8], self.text1[0:8])
        self.assertEqual(section_obj[0:8:2], self.text1[0:8:2])


if __name__ == '__main__':
    unittest.main()