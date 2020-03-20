import unittest
from image_squarifier import *


class image_squarifier(unittest.TestCase):
    def test_get_edge_colors(self):
        im = Image.new("RGB",(40,40),(30,10,20))
        edge_colors = get_edge_colors(im)
        self.assertEqual(len(edge_colors),156, "Should be 156")

    def test_get_avarages(self):
        self.assertEqual(get_averages([(100, 6, 30),
                                       (50, 4, 30),
                                       (20, 2, 6),
                                       (150, 50, 10)]), (80, 15.5, 19), "Should be (80,15.5,19)")

    def test_in_interval(self):
        self.assertTrue(in_interval(1, 180, 120.5), "Should be true")
        self.assertFalse(in_interval(0, 180, 120.5), "Should be False")
        self.assertTrue(in_interval(0, 100, 120.5), "Should be true")
        self.assertFalse(in_interval(1, 100, 120.5), "Should be False")


if __name__ == '__main__':
    unittest.main()
