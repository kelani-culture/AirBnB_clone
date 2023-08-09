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

# """a module that defines a FileStorage class"""
# import json
#
#
# def file_exists(file_str):
#     """a procedure that checks if a file exists"""
#     try:
#         with open(file_str, mode="r", encoding="utf-8") as _:
#             return True
#     except FileNotFoundError:
#         return False
#
#
# class FileStorage:
#     """a class that serves as a storage engine for other classes"""
#     __file_path = "file.json"
#     __objects = dict()
#
#     def all(self):
#         """a public instance method that returns all objects"""
#         return FileStorage.__objects
#
#     def new(self, obj):
#         """adds an instance to the FileStorage.__objects
#             dictionary"""
#         FileStorage.__objects[obj.id] = obj
#
#     def save(self):
#         """a public instance field that writes the FileStorage.__objects
#             to a file"""
#         list_objs = [item.to_dict() for item in FileStorage.__objects.values()]
#         if not list_objs or not len(list_objs):
#             with open(FileStorage.__file_path, mode="w",
#                       encoding="utf-8") as file:
#                 return json.dump([], file)
#         else:
#             with open(FileStorage.__file_path, mode="w",
#                       encoding="utf-8") as file:
#                 json.dump(list_objs, file)
#
#     def reload(self):
#         """a public instance methods that deserializes a JSON file
#         to FileStorage.__objects"""
#         if not file_exists(FileStorage.__file_path):
#             return
#         des_arr = []
#         des_dict = dict()
#         with open(FileStorage.__file_path, mode="r",
#                   encoding="utf-8") as f_ptr:
#             des_arr = json.load(f_ptr)
#             FileStorage.__objects = des_dict
#
