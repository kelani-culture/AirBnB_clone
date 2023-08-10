#!/usr/bin/python3
"""A test for review class"""

import unittest
from models.review import Review


class TestReview(unittest.TestCase):
    """
    An  implementation of the review class
    """
    def test_instance(self):
        review = Review()
        self.assertIsInstance(review.place_id, str)
        self.assertIsInstance(review.user_id, str)
        self.assertIsInstance(review.text, str)
