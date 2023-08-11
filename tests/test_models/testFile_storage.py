#!/usr/bin/python3

"""A test case for the file storage class"""
import tempfile
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
import shutil
import os

class TestFileStorage_base(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

        # Set the test JSON file path
        self.test_file_path = os.path.join(self.test_dir, "test_file.json")

        # Initialize a separate FileStorage instance for testing
        self.storage = FileStorage()
        self.storage._FileStorage__file_path = self.test_file_path

        # Create a BaseModel and save it
        self.base_model = BaseModel()
        self.storage.new(self.base_model)
        self.storage.save()

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_all(self):
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertIn("BaseModel.{}".format(self.base_model.id), all_objects)

    def test_new(self):
        new_model = BaseModel()
        self.storage.new(new_model)
        all_objects = self.storage.all()
        self.assertIn("BaseModel.{}".format(new_model.id), all_objects)

    def test_save_reload(self):
        new_model = BaseModel()
        self.storage.new(new_model)
        self.storage.save()

        # Create a new FileStorage instance for testing
        new_storage = FileStorage()
        new_storage._FileStorage__file_path = self.test_file_path
        new_storage.reload()

        all_objects = new_storage.all()
        self.assertIn("BaseModel.{}".format(self.base_model.id), all_objects)
        self.assertIn("BaseModel.{}".format(new_model.id), all_objects)

class TestFileStorage_user(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

        # Set the test JSON file path
        self.test_file_path = os.path.join(self.test_dir, "test_file.json")

        # Initialize a separate FileStorage instance for testing
        self.storage = FileStorage()
        self.storage._FileStorage__file_path = self.test_file_path

        # Create a User instance and save it
        self.user = User()  # Adjust this line based on your User class constructor
        self.storage.new(self.user)
        self.storage.save()

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_user_creation(self):
        # Test creating a User instance
        user = User()  # Adjust this line based on your User class constructor
        self.storage.new(user)
        all_objects = self.storage.all()
        self.assertIn("User.{}".format(user.id), all_objects)

    def test_user_save_reload(self):
        # Test saving and reloading a User instance
        new_user = User()  # Adjust this line based on your User class constructor
        self.storage.new(new_user)
        self.storage.save()

        # Create a new FileStorage instance for testing
        new_storage = FileStorage()
        new_storage._FileStorage__file_path = self.test_file_path
        new_storage.reload()

        all_objects = new_storage.all()
        self.assertIn("User.{}".format(self.user.id), all_objects)
        self.assertIn("User.{}".format(new_user.id), all_objects)
