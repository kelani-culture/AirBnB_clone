"""a module that defines a FileStorage class"""
import json
from models.base_model import BaseModel
from models.user import User


def file_exists(file_str):
    """a procedure that checks if a file exists"""
    try:
        with open(file_str, mode="r", encoding="utf-8") as _:
            return True
    except FileNotFoundError:
        return False


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
    __objects = dict()

    def all(self):
        """a public instance method that returns all objects"""
        return self.__objects #{key: val.to_dict() for key, val in self.__objects.items()}

    def new(self, obj):
        """adds an instance to the FileStorage.__objects
            dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj
        FileStorage.__objects[key] = obj

    def save(self):
        """a public instance field that writes the FileStorage.__objects
            to a file"""
        json_obj = {key: item.to_dict() for key,
                    item in FileStorage.__objects.items()}
        if not json_obj:
            with open(FileStorage.__file_path, mode="w",
                      encoding="utf-8") as file:
                return json.dump({}, file)
        else:
            with open(FileStorage.__file_path, mode="w",
                      encoding="utf-8") as file:
                json.dump(json_obj, file)

    def reload(self):
        """a public instance methods that deserializes a JSON file
            to FileStorage.__objects"""
        if not file_exists(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, mode="r",
                  encoding="utf-8") as f_ptr:
            FileStorage.__objects = json.load(f_ptr)
            for key, value in FileStorage.__objects.items():
                class_str = key.split(".")[0]
                instance = globals()[class_str](**value)

                for attr_name, attr_value in value.items():
                    if attr_name not in ['id', 'updated_at', 'created_at', '__class__']:
                        setattr(instance, attr_name, attr_value)
                self.__objects[key] = instance
                FileStorage.__objects[key] = instance
        return self.__objects
