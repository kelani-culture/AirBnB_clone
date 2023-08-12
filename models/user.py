#!/usr/bin/env python3
"""An implementation of the user class"""
from models.base_model import BaseModel
import datetime


class User(BaseModel):
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
    count = 0

    def __init__(self, *_, **kwargs):
        """the constructor function"""
        super().__init__(**kwargs)
        User.count += 1

    @staticmethod
    def reduce():
        """a public instance method that reduces the number of instances"""
        User.count -= 1

    def to_dict(self):
        """a public instance method that returns the dictionary
            representation of the instance"""
        all_attrs = {
                key: value
                for key, value in self.__dict__.items()
            }
        all_attrs.update({"__class__": self.__class__.__name__})
        if isinstance(self.created_at, datetime.datetime):
            all_attrs.update({"created_at":
                              self.created_at.isoformat()})
        if isinstance(self.updated_at, datetime.datetime):
            all_attrs.update({"updated_at":
                              self.updated_at.isoformat()})
        return all_attrs
