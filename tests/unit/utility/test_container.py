import unittest
from src.pynavy.utility.container import Container
from src.pynavy.utility.section import Section

class TestContainer(unittest.TestCase):
    def setUp(self):
        self.text1 = "0123456789"
        self.text2 = "Life without money is a hell"
        self.section_obj1 = Section(self.text1)
        self.section_obj2 = Section(self.text2)

    def test_size(self):
        container_obj = Container([self.section_obj1])
        self.assertEqual(container_obj.size(), 1)

    def test_create_start_indexes(self):
        container_obj = Container([self.section_obj1])
        start_indexes = container_obj.create_start_indexes(len(self.text1), 5)
        self.assertEqual(start_indexes, (0,5))
        start_indexes = container_obj.create_start_indexes(len(self.text1), 2)
        self.assertEqual(start_indexes, (0, 2, 4, 6, 8))
        start_indexes = container_obj.create_start_indexes(1, 2)
        self.assertEqual(start_indexes, (0,))
        start_indexes = container_obj.create_start_indexes(0, 2)
        self.assertEqual(start_indexes, ())

    def test_create_end_indexes(self):
        container_obj = Container([self.section_obj1])
        end_indexes = container_obj.create_end_indexes(len(self.text1), 5)
        self.assertEqual(end_indexes, (5,10))
        end_indexes = container_obj.create_end_indexes(len(self.text1), 2)
        self.assertEqual(end_indexes, (2, 4, 6, 8, 10))
        end_indexes = container_obj.create_end_indexes(1, 2)
        self.assertEqual(end_indexes, (1,))
        end_indexes = container_obj.create_end_indexes(0, 2)
        self.assertEqual(end_indexes, ())

    def test_create_start_end_indexes(self):
        container_obj = Container([self.section_obj1])
        start_end_indexes = container_obj.create_start_end_indexes(len(self.text1), 5)
        self.assertEqual(start_end_indexes, ((0,5), (5,10)))
        start_end_indexes = container_obj.create_start_end_indexes(len(self.text1), 2)
        self.assertEqual(start_end_indexes, ((0,2), (2,4), (4,6),(6, 8), (8, 10)))
        start_end_indexes = container_obj.create_start_end_indexes(len(self.text1)+1, 2)
        self.assertEqual(start_end_indexes, ((0,2), (2,4), (4,6),(6, 8), 
            (8, 10), (10, 11))
        )
        start_end_indexes = container_obj.create_start_end_indexes(1, 2)
        self.assertEqual(start_end_indexes, ((0,1),))
        start_end_indexes = container_obj.create_start_end_indexes(0, 2)
        self.assertEqual(start_end_indexes, ())

    def test_create_sections(self):
        container_obj = Container([self.section_obj1])
        sections = container_obj.create_sections(self.text1, 2)
        start_end_indexes = ((0,2), (2,4), (4,6),(6, 8), (8, 10))
        self.assertEqual(len(sections), len(start_end_indexes))
        for i in range(len(sections)):
            start, end = start_end_indexes[i]
            section = sections[i]
            self.assertEqual(section.get_elements(), self.text1[start:end])

    def test_create_section(self):
        container_obj = Container([self.section_obj1])
        section_obj = container_obj.create_section(self.text1, (4, 8))
        self.assertEqual(section_obj.get_elements(), self.text1[4:8])

    def test_contains_sections(self):
        container_obj = Container()
        self.assertTrue(container_obj.contains_sections([self.section_obj1]))
        self.assertFalse(container_obj.contains_sections([
            self.section_obj1, "section_obj"
        ]))

    def test_filter_section_qualify(self):
        container_obj = Container([self.section_obj1])
        self.assertTrue(container_obj.section_qualify(self.section_obj1))

    def test_filter_qualify_sections(self):
        container_obj = Container([self.section_obj1])
        self.assertEqual(container_obj.filter_qualify_sections(), 
        [self.section_obj1])

    def test_add_section(self):
        container_obj = Container()
        section_obj = Section(self.text1)
        self.assertEqual(container_obj.size(), 0)
        container_obj.add_section(section_obj)
        self.assertEqual(container_obj.size(), 1)
        with self.assertRaises(TypeError):
            container_obj.add_section("section_obj")

    
    def test_section_exists(self):
        container_obj = Container([self.section_obj1])
        container_obj.add_section(self.section_obj1)
        self.assertTrue(container_obj.section_exists(
            lambda x: x.get_elements() == self.text1)
        )
        self.assertFalse(container_obj.section_exists(
            lambda x: x.get_elements() == self.text2)
        )


    def test_filter_sections(self):
        container_obj = Container()
        container_obj.add_section(self.section_obj1)
        container_obj.add_section(self.section_obj2)
        filtered = container_obj.filter_sections(
            container_obj.get_sections(),
            lambda x: x.get_elements() == self.text2
        )
        self.assertEqual(len(filtered), 1)
        filtered = container_obj.filter_sections(
            container_obj.get_sections(),
            lambda x: x.get_elements() == ""
        )
        self.assertEqual(len(filtered), 0)
        filtered = container_obj.filter_sections(
            container_obj.get_sections(), 
            lambda x: True)
        self.assertEqual(len(filtered), 2)


    def test_remove_section(self):
        container_obj = Container()
        container_obj.add_section(self.section_obj1)
        container_obj.add_section(self.section_obj2)
        self.assertEqual(container_obj.size(), 2)
        container_obj.section_exists(lambda x: x.get_elements() == self.text1)
        container_obj.remove_section(lambda x: x.get_elements() == self.text1)
        self.assertEqual(container_obj.size(), 1)
        with self.assertRaises(Exception):
            # does not exists
            container_obj.remove_section(lambda x: x.get_elements() == "")

    def test_clear(self):
        container_obj = Container( 
            metadata={"keywords": ["john"], "size_chars":30000}
        )
        container_obj.add_section(self.section_obj1)
        self.assertEqual(container_obj.get_metadata_size(), 2)
        self.assertEqual(container_obj.size(), 1)
        container_obj.clear()
        self.assertEqual(container_obj.get_metadata_size(), 0)
        self.assertEqual(container_obj.size(), 0)

    def test_get_sections(self):
        container_obj = Container()
        container_obj.add_section(self.section_obj1)
        container_obj.add_section(self.section_obj2)
        sections = container_obj.get_sections()
        text_list = [self.text1, self.text2]
        for i in range(len(sections)):
            self.assertEqual(sections[i].get_elements(), text_list[i])

    def test_set_sections(self):
        container_obj = Container()
        self.assertEqual(container_obj.size(), 0)
        container_obj.set_sections([self.section_obj1, self.section_obj2])
        self.assertEqual(container_obj.size(), 2)
        with self.assertRaises(TypeError):
            container_obj.set_sections("sections")

    def test__contains__(self):
        container_obj = Container()
        container_obj.add_section(self.section_obj1)
        self.assertTrue(self.section_obj1 in container_obj)
        self.assertFalse(self.section_obj2 in container_obj)

    def test__iter__(self):
        container_obj = Container()
        container_obj.add_section(self.section_obj1)
        self.assertEqual(len(list(iter(container_obj))), 1)

    def test__next__(self):
        container_obj = Container()
        container_obj.add_section(self.section_obj1)
        container_obj.add_section(self.section_obj2)
        self.assertEqual(next(container_obj), self.section_obj1)
        self.assertEqual(next(container_obj), self.section_obj2)
        with self.assertRaises(StopIteration):
            while True:
                next(container_obj)

    def test__len__(self, /):
        container_obj = Container()
        self.assertEqual(len(container_obj), 0)
        container_obj.add_section(self.section_obj1)
        self.assertEqual(len(container_obj), 1)


    def test__bool__(self, /):
        container_obj = Container()
        self.assertFalse(bool(container_obj))
        container_obj.add_section(self.section_obj1)
        self.assertTrue(bool(container_obj))

    def test__getitem__(self, /):
        container_obj = Container()
        container_obj.add_section(self.section_obj1)
        container_obj.add_section(self.section_obj2)
        self.assertEqual(container_obj[0].get_elements(), 
            self.section_obj1.get_elements()
        )
        self.assertEqual(container_obj[0].get_elements(), 
            self.section_obj1.get_elements()
        )


if __name__ == '__main__':
    unittest.main()

