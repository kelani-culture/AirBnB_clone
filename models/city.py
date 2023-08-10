#!/usr/bin/env python3
"""An implementation of the city class"""
from models.base_model import BaseModel


class City(BaseModel):
    """city class"""
    state_id: str = ""
    name: str = ""
