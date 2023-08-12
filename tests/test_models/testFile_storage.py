#!/usr/bin/python3

"""A test case for the file storage class"""

import os
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
import tempfile
import models


class TestFileStorage_base(unittest.TestCase):
    """Test case for the test file storage class"""

    @classmethod
    def setUp(cls):
        models.storage.__file_path = 'test_file'
        with tempfile.NamedTemporaryFile(prefix=models.storage.__file_path,
                                         suffix=".json", delete=False) as file:
            cls.temp_file_path = file.name

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.temp_file_path):
            os.remove(cls.temp_file_path)

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


class TestFileStorage_user(TestFileStorage_base):
    """User test File storage that inherit from class 
    """

    def setUp(self):
        self.my_user = User()
        self.my_user.first_name = "Betty"
        self.my_user.last_name = "Bar"
        self.my_user.email = "airbnb@mail.com"
        self.my_user.password = "root"

    def test_new_save_reload(self):
        models.storage.new(self.my_user)
        models.storage.save()

        # Create a new FileStorage instance and reload data
        new_storage = FileStorage()
        new_storage.reload()

        # Retrieve the stored instance
        loaded_objects = new_storage.all()
        key = "User." + self.my_user.id
        self.assertIn(key, loaded_objects)
 
        # Retrieve the retrieved model
        retrieved_model = loaded_objects[key]
        self.assertEqual(retrieved_model.first_name, "Betty")

    def test_reload(self):
        storage = FileStorage()
        storage.reload()

        # Retrieve the stored instance and check if
        #the dynamically added attribute is present
        loaded_objects = storage.all()
        print("class name and id ", self.__class__.__name__, self.my_user.id)
        print("loaded objects")
        print(loaded_objects)
        print("======")
        self.assertTrue("User." + self.my_user.id in loaded_objects)
        retrieved_model = loaded_objects["User." + self.my_user.id]
        self.assertEqual(retrieved_model.first_name, "Betty")
        self.assertEqual(retrieved_model.password, "root")
        self.assertEqual(retrieved_model.email, "airbnb@mail.com")
