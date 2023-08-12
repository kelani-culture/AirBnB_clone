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
    count = 0

    def __init__(self, *_, **kwargs):
        """the constructor function"""
        if kwargs or kwargs.items():
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    if (value and type(value) == str):
                        format = "%Y-%m-%dT%H:%M:%S.%f"
                        setattr(self, key, datetime.datetime.strptime(value, format))
                elif key == "id":
                    if (is_uuid_valid(value)):
                        self.id = str(value)
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
        models.storage.new(self)
        if self.__class__.__name__ == "BaseModel":
            BaseModel.count += 1

    @staticmethod
    def reduce():
        """a public instance method that reduces the number of instances"""
        BaseModel.count -= 1

    def save(self):
        """a public instance method that updates the
            updated_at instance attribute with the current date time"""
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    # def update(self, *args, **kwargs):
    #     """a public instance method that updates or adds a new attribute
    #         to the instance"""
    #     print("dictionaries\n")
    #     print(models.storage.all())
    #     if args and len(args) % 2 == 0:
    #         pass
    #     elif kwargs and kwargs.items():
    #         pass

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

    def __str__(self):
        """a magic method that returns the printable
            representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
