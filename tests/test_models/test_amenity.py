#!/usr/bin/python3
"""test for amenity class"""
import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """implement test case for the amenity class"""

    def test_class_attr(self):
        amenity = Amenity()
        amenity.name = "Spider mobil"
        self.assertEqual(amenity.name, "Spider mobil")

    def test_instance(self):
        amenity = Amenity()
        self.assertEqual(amenity.name, str)
