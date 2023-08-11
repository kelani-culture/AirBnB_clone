#!/usr/bin/env python3
"""a module that defines utility functions for the console module"""

from . import amenity, base_model, city
from . import place, review, state
from . import storage, user
import cmd
import re

# globals
Amenity = amenity.Amenity
BaseModel = base_model.BaseModel
City = city.City
Place = place.Place
Review = review.Review
State = state.State
User = user.User
completion_classes = ["BaseModel", "State", "City",
                      "Amenity", "Place", "User", "Review"]


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


def parse_and_handle_arg(cls: str, method: str, raw_arg: str) -> None:
    """
    parse_and_handle_arg - this parses the passed argument,
    validates it and handles it
    it's always going to be in the format:
        cls.method([raw_arg])
    Parameters:
        cls: the class name
        method: the method name
        raw_arg: the unparsed arguments
    Returns:
        None
    """
    if cls not in completion_classes:
        return
    cls_key = ""
    arg_extractor = CmdArgToken()
    # if method in globals()[cls].__dict__.keys():
    match method:
        case "all":
            handle_all(cls)
        case "show":
            id = arg_extractor.get_arg_str(raw_arg)
            if id and len(id) > 1:
                handle_show(cls, id[1])
        case "count":
            handle_count(cls)
        case "update":
            #     if args and len(args) % 2 == 0:
            print("handling update")
        case "destroy":
            print("handling destroy")
        case _:
            return

    # if not raw_arg:
    #     print("no argument")
    #     print(f"class: {cls}, method: {method}")
    # else:
    #     print(f"class: {cls}, method: {method}, arg: {raw_arg}")


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


def handle_count(cls_name):
    """this handles counting the number of instances created
        based on a class"""
    count = globals()[cls_name].__dict__["count"]
    print(count)


class CmdArgToken():
    """a class that resolves a parsed command line argument
        to it's logical values"""
    def get_arg_str(self, line) -> list:
        """this resolves the argument to a string only"""
        arg_str_arr = re.findall(r"^(\"|\')([\w-]+)\1", line)
        if not arg_str_arr:
            print("invalid first argument!")
            return []
        return arg_str_arr[0]

    def get_arg_str_and_arg(self, line) -> list:
        """this resolves the argument to a string and comma-separated values"""
        return []

    def get_arg_str_and_kwarg(self, line) -> list:
        """this resolves the argument to a string and key-value pairs"""
        return []


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
