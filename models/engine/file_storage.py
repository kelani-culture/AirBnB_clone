#!/usr/bin/env python3
"""a module that defines a FileStorage class"""

import json


def file_exists(file_str):
    """a procedure that checks if a file exists"""
    try:
        with open(file_str, mode="r", encoding="utf-8") as _:
            return True
    except FileNotFoundError:
        return False


class FileStorage:
    """a class that serves as a storage engine for other classes"""
    __file_path = "file.json"
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
        list_objs = [item.to_dict() for item in FileStorage.__objects.values()]
        if not list_objs or not len(list_objs):
            with open(FileStorage.__file_path, mode="w",
                      encoding="utf-8") as file:
                return json.dump([], file)
        else:
            with open(FileStorage.__file_path, mode="w",
                      encoding="utf-8") as file:
                json.dump(list_objs, file)

    def reload(self):
        """a public instance methods that deserializes a JSON file
        to FileStorage.__objects"""
        if not file_exists(FileStorage.__file_path):
            return
        des_arr = []
        des_dict = dict()
        with open(FileStorage.__file_path, mode="r",
                  encoding="utf-8") as f_ptr:
            des_arr = json.load(f_ptr)
            FileStorage.__objects = des_dict
