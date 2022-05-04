import unittest
from src.pynavy.utility.equality import Equality

class TestContainer(unittest.TestCase):
    def setUp(self) -> None:
        self.equality_obj1 = Equality()
        self.equality_obj2 = Equality()

    def test__key(self):
        self.assertEqual(self.equality_obj1.__key(), self.equality_obj1.__key())
        self.assertNotEqual(self.equality_obj.__key(), self.equality_obj2.__key())

    def test__key(self):
        self.assertEqual(hash(self.equality_obj1), hash(self.equality_obj1))
        self.assertNotEqual(hash(self.equality_obj1), hash(self.equality_obj2))

    def test__eq__(self):
        self.assertTrue(self.equality_obj1 == self.equality_obj1)
        self.assertFalse(hash(self.equality_obj1) == hash(self.equality_obj2))

    def test__eq__(self):
        self.assertFalse(self.equality_obj1 != self.equality_obj1)
        self.assertTrue(hash(self.equality_obj1) != hash(self.equality_obj2))