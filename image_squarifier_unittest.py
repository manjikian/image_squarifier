import unittest
from image_squarifier import *


class image_squarifier(unittest.TestCase):
    def test_in_interval(self):
        self.assertTrue(in_interval(1, 180, 120.5), "Should be true")
        self.assertFalse(in_interval(0, 180, 120.5), "Should be False")
        self.assertTrue(in_interval(0, 100, 120.5), "Should be true")
        self.assertFalse(in_interval(1, 100, 120.5), "Should be False")

if __name__ == '__main__':
    unittest.main()
