#!/usr/bin/python3
"""Implementation of the amenity class"""

from models.base_model import BaseModel


class Place(BaseModel):
    """
    implementaation of amenity class that inherits from the Base class
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longtitude = 0.0
    amenity_ids = []
