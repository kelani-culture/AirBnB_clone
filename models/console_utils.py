#!/usr/bin/env python3
"""a module that defines utility functions for the console module"""

from . import base_model
from . import user
import cmd
import re
from . import storage

# globals
BaseModel = base_model.BaseModel
User = user.User
completion_classes = ["BaseModel", "State", "City", "Place", "User"]


def derive_type_from_string(string: str):
    """this derives a type from an input string based on its value"""
    float_pattern = r"^\d+\.\d+$"
    int_pattern = r"^\d+$"
    string_pattern = r"[^\d]+"

    if (re.match(float_pattern, string) is not None):
        return float
    elif (re.match(int_pattern, string) is not None):
        return int
    elif (re.match(string_pattern, string) is not None):
        return str
    else:
        return str


def handle_arg(args, command, parsed, handler=None):
    """
    handle_arg - this validates the argument passed and handles it
    it's always going to be in the format:
        comand [class_name] [id]
    Parameters:
        args: the number of argument expected to the command
        parsed: the arguments parsed
    Returns:
        None
    """
    cls_name = None
    if not handler:
        return

    if parsed:
        cls_name = parsed[0]
        if not (parsed[0] in globals()):
            print("** class doesn't exist **")
            return
    elif command == "all":
        pass
    else:
        print("** class name missing **")
        return

    match args:
        case 0:
            handler(cls_name)
        case 1:
            handler(cls_name)
        case 2:
            try:
                instance_id = parsed[1]
            except IndexError:
                print("** instance id missing **")
                return
            handler(cls_name, instance_id)
        case 4:
            try:
                instance_id = parsed[1]
            except IndexError:
                print("** instance id missing **")
                return
            try:
                field_key = parsed[2]
            except IndexError:
                print("** attribute name missing **")
                return
            try:
                field_value = parsed[3]
            except IndexError:
                print("** value missing **")
                return
            handler(cls_name, instance_id, field_key, field_value)
        case _:
            pass


def suggest(text, line):
    """comes up with auto-completion based on the text passed in"""
    if not text:
        completions = completion_classes[:]
    else:
        completions = [item for
                       item in completion_classes if item.startswith(text)]
    return completions


def handle_create(cls_name):
    """this handles the creation of new instances and writing
        to a JSON file"""
    new_instance = (globals()[cls_name])()
    new_instance.save()
    print(new_instance.id)


def handle_show(cls_name, id):
    """this handles the printing of string representation of
        an instance based on a class"""
    res_objs = storage.all()
    key = f"{cls_name}.{id}"
    try:
        res = res_objs[key]
    except KeyError:
        print("** no instance found **")
        return
    print(res)


def handle_destroy(cls_name, id):
    """this handles the destruction of instances
        based on a class"""
    res_objs = storage.all()
    key = f"{cls_name}.{id}"
    try:
        _ = res_objs[key]
    except KeyError:
        print("** no instance found **")
        return
    del res_objs[key]
    storage.save()


def handle_all(cls_name):
    """this handles the printing of the string representation of all
        instances based or not on the class name"""
    if not cls_name:
        res_insts = {key: value for key,
                     value in storage.all().items()}
    else:
        res_insts = {key: value for key,
                     value in storage.all().items()
                     if key.startswith(cls_name)}
    res_array = []
    for key, value in res_insts.items():
        res_array.append(value.__str__())
    print(res_array)


def handle_update(cls_name, id, key, value):
    """this handles the updating of fields of an entry
        in the JSON file"""
    res_key = f"{cls_name}.{id}"
    try:
        _ = storage.all()[res_key]
    except KeyError:
        print("** no instance found **")
        return
    setattr(storage.all()[res_key], str(key), value)
    storage.save()


class CompletionClass(cmd.Cmd):
    """auto-completion class for the HbnbCommand class"""

    def complete_create(self, text, line, _, __):
        """auto-completion for all command"""
        return suggest(text, line)

    def complete_show(self, text, line, _, __):
        """auto-completion for show command"""
        return suggest(text, line)

    def complete_all(self, text, line, _, __):
        """auto-completion for all command"""
        return suggest(text, line)

    def complete_destroy(self, text, line, _, __):
        """auto-completion for destroy command"""
        return suggest(text, line)

    def complete_update(self, text, line, _, __):
        """auto-completion for update command"""
        return suggest(text, line)
