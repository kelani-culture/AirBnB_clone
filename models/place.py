#!/usr/bin/python3
"""Implementation of the amenity class"""

from models.base_model import BaseModel


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
        super().__init__(**kwargs)
        self.city_id = Place.city_id
        self.user_id = Place.user_id
        self.name = Place.name
        self.description = Place.description
        self.number_rooms = Place.number_rooms
        self.max_guest = Place.max_guest
        self.price_by_night = Place.price_by_night
        self.latitude = Place.latitude
        self.longitude = Place.longitude
        self.amenity_ids = Place.amenity_ids
        Place.count += 1

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
