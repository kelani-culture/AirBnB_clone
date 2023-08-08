#!/usr/bin/python3
""" Implementation of the FileStorage class"""
import json
from models.base_model import BaseModel


class FileStorage:
    """
    FileStorage serializes instances to a JSON file and 
    deserializes JSON file to instance

    __file_path - string path to the JSON file
    __objects - an empty dictionary that will store all objects

    new - A method that create a dictionary object
    save - A method that save the dict object to json file
    reload - A method that load a json file
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        A method that returns the dictionary objects
        """
        return self.__objects

    def new(self, obj):
        """ Create a dictitionary object """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Save a python object to a json file"""
        ser_obj = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as json_file:
            json.dump(ser_obj, json_file)

    def reload(self):
        """load a file from json"""
        try:
            with open(self.__file_path) as open_jsonFile:
                self.__objects = json.load(open_jsonFile)
                for key, val in self.__objects.items():
                    class_name = key.split('.')[0]
                    instance = globals()[class_name](**val)
                    self.__objects[key] = instance
                return self.__objects
        except FileNotFoundError:
            pass
