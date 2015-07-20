
import unittest

from spike import square


class TestSquare(unittest.TestCase):

    def test_square(self):
        self.assertEqual(0, square(0))
        self.assertEqual(49, square(7))

    def test_negatives(self):
        self.assertEqual(49, square(-7))


if __name__ == '__main__':
    unittest.main()
