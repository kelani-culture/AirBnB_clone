#!/usr/bin/env python3
"""a module that defines a FileStorage class"""

import json


class FileStorage:
    """a class that serves as a storage engine for other classes"""
    __file_path = ""
    __objects = dict()

    def all(self):
        """a public instance method that returns all objects"""
        return FileStorage.__objects

    def new(self, obj):
        """adds an instance to the FileStorage.__objects
            dictionary"""
        FileStorage.__objects[obj.id] = obj

    def save(self):
        """a public instance field that writes the FileStorage.__objects
            to a file"""
        list_objs = [FileStorage.__objects[item] for
                     item in FileStorage.__objects.keys()]
        if not list_objs:
            with open(FileStorage.__file_path, mode="w",
                      encoding="utf-8") as file:
                return json.dump([], file)
        else:
            list_objs = [obj.to_dictionary() for obj in list_objs]
            with open(FileStorage.__file_path, mode="w",
                      encoding="utf-8") as file:
                json.dump(list_objs, file)

    def reload(self):
        """a public instance methods that deserializes a JSON file
        to FileStorage.__objects"""
        pass
