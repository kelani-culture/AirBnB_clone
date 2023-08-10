#!/usr/bin/python3
"""Test case for User class"""
import unittest
from models.user import User


class TestUser(unittest.TestCase):
    """A test for the user class
    """

    def setUp(self):
        self.user = User()
        self.user.first_name = "Miguel"
        self.user.last_name = "Ohara"
        self.user.password = "spiderman2099"
        self.user.email = "MiguelOhara@spiderman2099.com"

    def test_instance_class_attr(self):
        """Test for instance of the class attr
        """
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.password, str)

    def test_value(self):
        """Test for attribute value"""
        self.assertEqual(self.user.first_name, "Miguel")
        self.assertEqual(self.user.last_name, "Ohara")
        self.assertEqual(self.user.email, "MiguelOhara@spiderman2099.com")
        self.assertEqual(self.user.password, "spiderman2099")
