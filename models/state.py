#!/usr/bin/env python3
"""An implementation of the State class"""

from models.base_model import BaseModel


class State(BaseModel):
    """the State class
        name - name of the state
    """
    name: str = ""
