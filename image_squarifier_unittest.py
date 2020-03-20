import unittest
from image_squarifier import *
from unittest_variables import *


class image_squarifier(unittest.TestCase):

    def test_get_edge_colors(self):
        edge_colors = get_edge_colors(im_v)
        self.assertEqual(len(edge_colors), 196, "Should be 156")
        self.assertEqual(edge_colors[0], (30, 10, 20), "Should be (30,10,20)")
        self.assertEqual(edge_colors[72], (30, 10, 20), "Should be (30,10,20)")

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

    def test_resize_im(self):
        new_im = resize_im(40, im_v)
        self.assertLessEqual(new_im.size[1], 40, "Should be <= 40")
        new_im = resize_im(40, small_im_v)
        self.assertLessEqual(new_im.size[1], 40, "Should be <= 40")
        new_im = resize_im(40, im_h)
        self.assertLessEqual(new_im.size[0], 40, "Should be <= 40")
        new_im = resize_im(40, small_im_h)
        self.assertLessEqual(new_im.size[0], 40, "Should be <= 40")

    def test_paste_in_middle(self):
        new_im = paste_in_middle(im_v, small_im_v)
        self.assertEqual(new_im.size, (40, 60), "Should be (40,60)")
        self.assertEqual(new_im.getpixel((0, 0)), (30, 10, 20), "Should be (30, 10, 20)")
        self.assertEqual(new_im.getpixel((20, 30)), (60, 20, 40), "Should be (60, 20, 40)")
        self.assertEqual(new_im.getpixel((9, 14)), (30, 10, 20), "Should be (30, 10, 20)")
        self.assertEqual(new_im.getpixel((10, 15)), (60, 20, 40), "Should be (60, 20, 40)")
        self.assertEqual(new_im.getpixel((30, 35)), (30, 10, 20), "Should be (30, 10, 20)")
        self.assertEqual(new_im.getpixel((29, 34)), (60, 20, 40), "Should be (60, 20, 40)")


if __name__ == '__main__':
    unittest.main()
