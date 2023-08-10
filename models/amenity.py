#!/usr/bin/env python3
"""An implementation of the amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    name: str = ""
