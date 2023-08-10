#!/usr/bin/env python3
"""An implementation of the user class"""
from models.base_model import BaseModel


class User(BaseModel):
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
