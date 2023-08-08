#!/usr/bin/python3

""" The base model class for every object"""
import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel - the base class for all classes
    id - assign a unique id for each instance creation
    created_at - date and time of when the instance was created
    updated_at - date and time of when the instance was updated at

    save - for updating the public instance with the current time
    to_dict - return a dict of public instance and class
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    # return string representation of the BaseModel data
    def __str__(self):
        return (f"[{self.__class__.__name__}] ({self.id}) {vars(self)}")

    # for updating the the public instance with the current time
    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        convert both updated_at and created_at to an isoformat date time
        """
        in_dict = self.__dict__
        in_dict['created_at'] = (
                   datetime.fromisoformat(in_dict['created_at'].isoformat())
                )
        in_dict['updated_at'] = (
                 datetime.fromisoformat(in_dict['updated_at'].isoformat())
            )
        return in_dict
