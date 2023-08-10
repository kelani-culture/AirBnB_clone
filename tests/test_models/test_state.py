#!/usr/bin/python3
"""Test for state class"""

import unittest
from models.state import State


class TestState(unittest.TestCase):
    """A test for the state class attr"""

    def test_attr(self):
        state = State()
        state.name = "New York"
        self.assertEqual(state.name, "New York")

    def test_check_instance(self):
        state = State()
        self.assertIsInstance(state.name, str)
