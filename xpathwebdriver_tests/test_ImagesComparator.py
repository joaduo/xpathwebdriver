# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import unittest
#from smoothtest.webunittest.ImagesComparator import ImagesComparator
import os
from xpathwebdriver.ImagesComparator import ImagesComparator


class TestImagesComparator(unittest.TestCase):
    def test_comparator(self):
        ic = ImagesComparator()
        base = os.path.join(os.path.dirname(__file__), 'img')
        a_file = os.path.join(base, 'street.jpg') 
        b_file = os.path.join(base, 'street_diff.jpg')
        diff = os.path.join(base, 'diff.jpg')
        self.assertFalse(ic.compare(a_file, b_file, threshold=100))
        self.assertTrue(ic.compare(a_file, b_file, threshold=50))
        ic.create_diff(a_file, b_file, diff, crop_threshold=100)
        os.remove(diff)


if __name__ == "__main__":
    unittest.main()
