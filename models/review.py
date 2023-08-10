#!/usr/bin/env python3
"""An implementation of the review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    place_id: str = ""
    user_id: str = ""
    text: str = ""
