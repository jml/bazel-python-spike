
from unittest import TestCase

from spike import square


class TestSquare(TestCase):

    def test_square(self):
        self.assertEqual(0, square(0))
        self.assertEqual(49, square(7))

    def test_negatives(self):
        self.assertEqual(49, square(-7))

