#!/usr/bin/python3

"""A test case for the file storage class"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import json
import os

def read_files(file):
    try:
        with open(file) as f:
            json.load(file)
    except FileNotFoundError:
        pass

class TestFileStorage(unittest.TestCase):
    """A test case for every method in the FileStorage"""

    def setUp(self):
        self.my_model = BaseModel()
        self.my_model.name = "john"
        self.my_model.number = 99
        self.file_storage = FileStorage()

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = BaseModel()
        cls.model.name = "Mike"
        cls.model.number = 100
        cls.file_stor = FileStorage()

        obj_id = f"{cls.model.__class__.__name__}.{cls.model.id}"
        cls.all_dict = {obj_id: cls.model.to_dict()}
        with open("test_file.json", 'w') as json_file:
            json.dump(cls.all_dict, json_file)

    def test_all(self):
        """Test if the the all method
        return a dictionary object
        """
        self.file_storage.new(self.my_model)
        all_objs = self.file_storage.all()
        self.assertIsInstance(all_objs, dict)

        obj_id = f"{self.my_model.__class__.__name__}.{self.my_model.id}"
        all_dict = {obj_id: self.my_model.to_dict()}
        self.assertEqual(all_objs, all_dict)

    def test_save(self):
        """ Test for the serialization of the json file_storage
        """
