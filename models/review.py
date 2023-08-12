#!/usr/bin/env python3
"""An implementation of the review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class
    """
    place_id: str = ""
    user_id: str = ""
    text: str = ""
    count = 0

    def __init__(self, *_, **kwargs):
        """the constructor function"""
        super().__init__(**kwargs)
        self.place_id = Review.place_id
        self.user_id = Review.user_id
        self.text = Review.text
        Review.count += 1

    @staticmethod
    def reduce():
        """a public instance method that reduces the number of instances"""
        Review.count -= 1

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
