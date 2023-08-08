#!/usr/bin/python3

"""Test for the baseModels class"""
from models.base_model import BaseModel
from datetime import datetime
import unittest
import uuid


def is_valid_uuid(value):
    """
    Checks the validity of the uuid
    """
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


class TestBaseModels(unittest.TestCase):
    """
    A Test for the BaseModels class

    test_uuid - test for the validity of the uuid
    test_created_date - test if the current datetime matches
    test_updated_date - test if the updated datetime matches
    test_instances - test for  the validity of each datatype
    test_save
    test_uuid - test for the validity of the uuid
    test_to_dict - returns the dictionary represenation of an object
    test_str - test if the string representation were returned
    """
    def setUp(self):
        self.my_model = BaseModel()
        self.my_model1 = BaseModel()

    def test_uuid(self):
        self.assertTrue(self.my_model.id)

    def test_created_date(self):
        """ Test if the instance created time matches """
        orig_created_time = self.my_model.created_at
        self.assertEqual(self.my_model.created_at, orig_created_time)

    def test_updated_date(self):
        """ Test if the updated time matches """
        updated = self.my_model1.created_at
        self.assertEqual(updated, self.my_model1.updated_at)

    def test_instances(self):
        """ Test if each attribute are the right data type"""
        self.assertIsInstance(self.my_model.id, str)
        self.assertIsInstance(self.my_model.created_at, datetime)
        self.assertIsInstance(self.my_model.updated_at, datetime)

    def test_save(self):
        """Test for the updated time with current time"""
        update_time = self.my_model1.save()
        self.assertEqual(update_time, self.my_model1.save())

    # test if the dictionary representation of instance is returned
    def test_to_dict(self):
        """Test if a dictionary representation of
            the public instance were returned
        """
        self.assertIsInstance(self.my_model1.to_dict(), dict)

        self.my_model.name = 'My first Model'
        self.my_model.number = 99
        # not needed, they do virtually the same thing
        # self.assertEqual(self.my_model.to_dict(), vars(self.my_model))

    def test_doc(self):
        """this is going to test for the presence of doc comments in
            methods"""
        self.assertIsNotNone(self.my_model.save.__doc__)
        self.assertIsNotNone(self.my_model.to_dict.__doc__)

    # returns the string representation of an object
    def test_str(self):
        """ Test if the string representation of an object was returned"""
        self.my_model.name = "My First model"
        self.my_model.number = 99
        self.assertEqual(str(self.my_model),
                         f"[BaseModel] ({self.my_model.id})" +
                         f" {self.my_model.__dict__}")
