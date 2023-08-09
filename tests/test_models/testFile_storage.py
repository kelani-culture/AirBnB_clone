#!/usr/bin/python3

"""A test case for the file storage class"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import models


class TestFileStorage(unittest.TestCase):
    """A test case for every method in the FileStorage"""
    
    def setUp(self):
        self.my_model = BaseModel()


    def test_all(self):
        """Test if the the all method
        return a dictionary object
        """
        self.my_model.name = "john"
        self.my_model.number = 99
        self.my_model.save()
        all_objs = models.storage.all()

        self.assertIsInstance(all_objs, dict)
