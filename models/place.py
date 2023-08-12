#!/usr/bin/python3
"""Implementation of the amenity class"""

from models.base_model import BaseModel
import datetime


class Place(BaseModel):
    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity_ids: list = []
    count = 0

    def __init__(self, *_, **kwargs):
        """the constructor function"""
        Place.count += 1

    @staticmethod
    def reduce():
        """a public instance method that reduces the number of instances"""
        Place.count -= 1

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
