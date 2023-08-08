#!/usr/bin/python3
""" Implementation of the FileStorage class"""
import json
import uuid

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
        key = f"{self.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Save a python object to a json file"""
        with open(self.__file_path, 'w') as json_file:
            json.dump(self.__objects, json_file)

    def reload(self):
        """load a file from json"""
        try:
            with open(self.__file_path) as open_jsonFile:
                self.__objects = json.load(open_jsonFile) 
        except FileNotFoundError:
            return
        else:
            return self.__objects
