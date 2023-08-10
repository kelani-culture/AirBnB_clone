#!/usr/bin/env python3
"""An implementation of the State class"""

from models.base_model import BaseModel


class State(BaseModel):
    """the State class
        name - name of the state
    """
    name: str = ""

    def __init__(self, *_, **kwargs):
        """the constructor function"""
        super().__init__(**kwargs)
        self.name = State.name

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
