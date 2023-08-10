#!/usr/bin/env python3
import datetime
import models
import uuid

""" the module that defines the base model class """


def is_uuid_valid(uuid_string):
    """a function that checks if a uuid is valid"""
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string
    except ValueError:
        return False


class BaseModel:
    """a class that defines a base model"""
    def __init__(self, *_, **kwargs):
        """the constructor function"""
        if kwargs or kwargs.items():
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                else:
                    self.__dict__[key] = value
                if key == "created_at":
                    if (value and type(value) == str):
                        self.created_at = datetime.datetime.fromisoformat(value)
                        self.updated_at = self.created_at
                if key == "id":
                    if (is_uuid_valid(value)):
                        self.id = value
            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs.keys():
                self.created_at = datetime.datetime.now()
                self.updated_at = self.created_at
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
        models.storage.new(self)

    def save(self):
        """a public instance method that updates the
            updated_at instance attribute with the current date time"""
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """a public instance method that returns the dictionary
            representation of the instance"""
        all_attrs = {
                key: value
                for key, value in self.__dict__.items()
            }
        all_attrs.update({"__class__": self.__class__.__name__})
        all_attrs.update({"created_at":
                          self.created_at.isoformat()})
        all_attrs.update({"updated_at":
                          self.updated_at.isoformat()})
        return all_attrs

    def __str__(self):
        """a magic method that returns the printable
            representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
