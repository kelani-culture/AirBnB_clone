#!/usr/bin/python3

"""A test case for the file storage class"""
import tempfile
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import models
import json
import os


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        # Set the temporary directory as the file storage path
        models.storage.__file_path = os.path.join(self.temp_dir.name, "file.json")

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_new_save_reload(self):
        """Test for the new and save method"""
        # Create an instance of BaseModel
        my_model = BaseModel()
        my_model.name = "test_name"

        # Save the instance using the FileStorage
        models.storage.new(my_model)
        models.storage.save()

        # Create a new FileStorage instance and reload data
        new_storage = FileStorage()
        new_storage.reload()

        # Retrieve the stored instance
        loaded_objects = new_storage.all()
        key = "BaseModel." + my_model.id
        self.assertIn(key, loaded_objects)
        
        # Retrieve the retrieved model
        retrieved_model = loaded_objects[key]
        self.assertEqual(retrieved_model.name, "test_name")

    def test_reload(self):
        """Test for the reload method"""
        # Create an instance of BaseModel and save it
        my_model = BaseModel()
        my_model.name = "test_reload"
        my_model.save()

        # Create a new FileStorage instance and reload data
        storage = FileStorage()
        storage.reload()

        # Retrieve the stored instance and check if
        #the dynamically added attribute is present
        loaded_objects = storage.all()
        self.assertTrue("BaseModel." + my_model.id in loaded_objects)
        retrieved_model = loaded_objects["BaseModel." + my_model.id]
        self.assertEqual(retrieved_model.name, "test_reload")
