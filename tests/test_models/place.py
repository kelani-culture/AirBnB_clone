#!/usr/bin/python3
"""test for place class"""

from models.place import Place
import unittest

class TestPlace(unittest.TestCase):
    """
    Implementation test for the amenity class
    """
    def test_instance(self):
        place = Place()
        self.assertIsInstance(place.city_id, str)
        self.assertIsInstance(place.user_id, str)
        self.assertIsInstance(place.name, str)
        self.assertIsInstance(place.description, str)
        self.assertIsInstance(place.number_rooms, int)
        self.assertIsInstance(place.number_bathrooms, int)
        self.assertIsInstance(place.max_guest, int)
        self.assertIsInstance(place.price_by_night, int)
        self.assertIsInstance(place.latitude, float)
        self.assertIsInstance(place.longtitude, float)
        self.assertIsInstance(place.amenity_ids, list)
