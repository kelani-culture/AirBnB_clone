#!/usr/bin/python3

"""Test for the baseModels class"""
import models
from models.base_model import BaseModel
from datetime import datetime
import unittest
import uuid
import json
import os
import time
import models.base_model
from models.engine.file_storage import FileStorage


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


class TestBase(unittest.TestCase):
    """Test cases for the `Base` class.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_initialization_positive(self):
        """Test passing cases `BaseModel` initialization.
        """
        b1 = BaseModel()
        b2_uuid = str(uuid.uuid4())
        b2 = BaseModel(id=b2_uuid, name="The weeknd", album="Trilogy")
        self.assertIsInstance(b1.id, str)
        self.assertIsInstance(b2.id, str)
        self.assertEqual(b2_uuid, b2.id)
        self.assertEqual(b2.album, "Trilogy")
        self.assertEqual(b2.name, "The weeknd")
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertEqual(str(type(b1)),
                         "<class 'models.base_model.BaseModel'>")

    def test_dict(self):
        """Test method for dict"""
        b1 = BaseModel()
        b2_uuid = str(uuid.uuid4())
        b2 = BaseModel(id=b2_uuid, name="The weeknd", album="Trilogy")
        b1_dict = b1.to_dict()
        self.assertIsInstance(b1_dict, dict)
        self.assertIn('id', b1_dict.keys())
        self.assertIn('created_at', b1_dict.keys())
        self.assertIn('updated_at', b1_dict.keys())
        self.assertEqual(b1_dict['__class__'], type(b1).__name__)

    def test_save(self):
        """Test method for save"""
        b = BaseModel()
        time.sleep(0.5)
        date_now = datetime.now()
        b.save()
        diff = b.updated_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_save_storage(self):
        """Tests that storage.save() is called from save()."""
        b = BaseModel()
        b.save()
        key = "{}.{}".format(type(b).__name__, b.id)
        d = {key: b.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as f:
            self.assertEqual(len(f.read()), len(json.dumps(d)))
            f.seek(0)
            self.assertEqual(json.load(f), d)

    def test_str(self):
        """Test method for str representation"""
        b1 = BaseModel()
        string = f"[{type(b1).__name__}] ({b1.id}) {b1.__dict__}"
        self.assertEqual(b1.__str__(), string)


class TestBaseModel(unittest.TestCase):
    """Test the class ``BaseModel``"""

    def setUp(self):
        """ Run before every test case"""
        pass

    def test_module_doc(self):
        """Test models.base_model module for documentation"""
        self.assertIsNotNone(models.base_model.__doc__)

    def test_class_doc(self):
        """Test ``BaseModel`` class for documentation"""
        self.assertIsNotNone(BaseModel.__doc__)

    def test_method_docs(self):
        """Test methods in ``BaseModel`` for documentation"""
        methods = [
            BaseModel.__init__,
            BaseModel.__str__,
            BaseModel.save,
            BaseModel.to_dict,
        ]
        for meth in methods:
            self.assertIsNotNone(meth.__doc__)

    def test_initial_attribute(self):
        """Test object id"""
        test_model = BaseModel()
        test_model2 = BaseModel()

        # check if id exists, not NULL and a string
        self.assertTrue(hasattr(test_model, "id"))
        self.assertIsNotNone(test_model.id)
        self.assertIsInstance(test_model.id, str)

        # Check if id is uuid
        self.assertTrue(uuid.UUID(test_model.id))

        # Check if two instances have the same id
        self.assertNotEqual(test_model.id, test_model2.id)

        # Check if created_at exist, not NULL, and it's from datetime
        self.assertTrue(hasattr(test_model, "created_at"))
        self.assertIsNotNone(test_model.created_at)
        self.assertIsInstance(test_model.created_at, datetime)

        # Check if updated_at exist, not NULL, and it's from datetime
        self.assertTrue(hasattr(test_model, "updated_at"))
        self.assertIsNotNone(test_model.updated_at)
        self.assertIsInstance(test_model.updated_at, datetime)

        self.assertTrue(hasattr(test_model, "__class__"))
        self.assertIsNotNone(test_model.__class__)
        self.assertIsInstance(test_model.__class__, object)
        # Check that *args was not used
        test_with_arg = BaseModel("args")
        self.assertNotIn("args", test_with_arg.__dict__)

        # Check if __str__ prints correct output
        str_ = "[BaseModel] ({}) {}".format(test_model.id, test_model.__dict__)
        self.assertEqual(str(test_model), str_)

        old = test_model.updated_at
        test_model.save()
        self.assertGreater(test_model.updated_at, old)

    def test_kwargs_input(self):
        """Test ``BaseModel`` initialization with kwargs"""
        dic = {
            "id": "test_id",
            "created_at": "2023-08-09T12:34:56.789012",
            "updated_at": "2023-08-09T13:45:12.345678",
            "name": "Wills",
            "value": 42,
        }
        test_model = BaseModel(**dic)

        self.assertEqual(test_model.name, "Wills")
        self.assertEqual(test_model.value, 42)
        self.assertIsInstance(test_model.created_at, datetime)
        self.assertIsInstance(test_model.updated_at, datetime)

    def test_to_dict_data_type(self):
        """Test each data type after ``to_dict``"""
        test_model = BaseModel()
        test_model.name = "Sabah"
        test_model.age = "lol"
        test_model.num = 12
        test_model.float_num = 12.21
        test_model.bool_val = True

        test_dict = test_model.to_dict()

        self.assertIsInstance(test_dict, dict)
        self.assertEqual(test_dict["__class__"], "BaseModel")
        self.assertEqual(test_dict["id"], test_model.id)
        self.assertEqual(test_dict["name"], "Sabah")
        self.assertEqual(test_dict["age"], "lol")
        self.assertEqual(test_dict["num"], 12)
        self.assertEqual(test_dict["float_num"], 12.21)
        self.assertEqual(test_dict["bool_val"], True)


if __name__ == "__main__":
    unittest.main()
