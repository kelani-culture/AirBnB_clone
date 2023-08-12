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

    if args == 0:
        handler(cls_name)
    elif args == 1:
        handler(cls_name)
    elif args == 2:
        try:
            instance_id = parsed[1]
        except IndexError:
            print("** instance id missing **")
            return
        handler(cls_name, instance_id)
    elif args == 4:
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
    else:
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

    if method == "all":
        handle_all(cls)
    elif method == "show":
        id = arg_extractor.get_arg_str(raw_arg)
        if id and len(id) > 1:
            handle_show(cls, id[1])
    elif method == "count":
        handle_count(cls)
    elif method == "create":
        handle_create(cls)
    elif method == "update":
        result_list = arg_extractor.get_arg_str_and_arg(raw_arg)
        result_dict = arg_extractor.get_arg_str_and_kwarg(raw_arg)
        if (result_dict):
            return
        elif (result_list):
            first_key = [item for item in result_list.keys()][0]
            first_value = [item for item in result_list.values()][0]
            handle_parsed_update(cls, first_key, **first_value)
        else:
            pass
    elif method == "destroy":
        id = arg_extractor.get_arg_str(raw_arg)
        if id and len(id) > 1:
            handle_destroy(cls, id[1])
    else:
        return


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
    globals()[cls_name].reduce()
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


def handle_parsed_update(cls_name, id, **kwargs):
    """this handles the updating of fields of an entry
        in the JSON file as manually parsed from the command line"""
    res_key = f"{cls_name}.{id}"
    try:
        _ = storage.all()[res_key]
    except KeyError:
        print("** no instance found **")
        return
    for key, value in kwargs.items():
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
            print("** instance id missing **")
            return []
        return arg_str_arr[0]

    def get_arg_str_and_arg(self, line) -> dict:
        """
        this resolves the argument to a string and comma-separated values
        based on the assumption that values will
        either be strings, numbers or array of strings only
        while keys will be strings only
        """
        split_tok = re.finditer(r"((([^,]+))\s*,?\s*)|(\[.*\])", line)
        split_tok = [i.group() for i in split_tok]
        join = False
        failed = False
        arg_list = []
        tmp_list = []
        if not split_tok:
            print("** instance id missing **")
            return {}
        for tok in split_tok:
            test_contain = re.findall(r"\[\s*(\"|\')([\w\@]+)\1\s*\]", tok)
            if (test_contain):
                tmp_list.append(test_contain[0][1])
                arg_list.append(tmp_list)
                tmp_list = []
                join = False
                continue
            test_open = re.findall(r"\[\s*(\"|\')([\w\@]+)\1\s*,\s*", tok)
            if test_open:
                tmp_list.append(test_open[0][1])
                join = True
                continue
            if join:
                test_close = re.findall(r"\s*(\"|\')([\w\@]+)\1\s*\]\s*,?\s*", tok)
                if test_close:
                    tmp_list.append(test_close[0][1])
                    join = False
                    if tmp_list:
                        arg_list.append(tmp_list)
                        tmp_list = []
                    continue
                else:
                    test_between = re.findall(r"\s*(\"|\')([\w\@]+)\1\s*,\s*", tok)
                    if test_between:
                        tmp_list.append(test_between[0][1])
                        join = True
            else:
                test_str_dig = re.findall(r"\s*((\"|\')([\w\@-]+)\2)|(\d+)\s*", tok)
                if test_str_dig:
                    if not len(test_str_dig[0]) == 4:
                        failed = True
                        break
                    if (test_str_dig[0][3]):
                        empty_s = re.search("^\s*\"\s*$", test_str_dig[0][3])
                        if empty_s:
                            failed = True
                            break
                        arg_list.append(test_str_dig[0][3])
                    else:
                        arg_list.append(test_str_dig[0][2])
        if not len(arg_list) % 2 or failed:
            return {}
        res_dict = []
        res_list = arg_list[1:]
        for idx, item in enumerate(res_list):
            if type(item) == str:
                dig_test = re.search(r"^\d+$", item)
                if dig_test:
                    res_list[idx] = int(item)
        for idx, item in enumerate(res_list):
            if idx % 2 == 0 or not idx:
                res_dict.append((item, res_list[idx + 1]))
        res = {arg_list[0]: dict(res_dict)}
        return res

    def get_arg_str_and_kwarg(self, line) -> dict:
        """this resolves the argument to a string and key-value pairs"""
        failed = False
        split_tok = line.split(",")
        tmp_dict = {"key": "value"}
        if len(split_tok) <= 1:
            failed = True

        test_id = re.findall(r"\s*((\"|\')([\w-]+)\2)\s*", split_tok[0])
        if not test_id:
            failed = True
            return tmp_dict
        if failed:
            return tmp_dict

        arg_tok = ",".join(split_tok[1:])  # i doubt this splitting mechanism
        print(arg_tok)
        kwarg_raw = re.findall("^\s*\{(.*)\}\s*$", arg_tok)
        kwarg_tok = []
        if kwarg_raw:
            kwarg_tok = kwarg_raw[0].split(",")
            for idx, item in enumerate(kwarg_tok):
                kwarg_tok[idx] = item.split(":")
        else:
            failed = True
            return tmp_dict
        print("kwarg tokens")

        for item in kwarg_tok:
            print(item)
            for spot in item:
                test_empty = re.search(r"^\s*(\"|\')?\s*$", str(spot))
                if test_empty:
                    failed = True
                    break
            if failed:
                break
        if failed:
            return tmp_dict

        # extract arrays
        # join = False
        # test_contain = re.findall(r"\[\s*(\"|\')([\w\@]+)\1\s*\]", tok)
        return tmp_dict

        # extract key-value pairs
        key_list = []
        value_list = []
        for idx, item in enumerate(kwarg_tok):
            for ind, tok in enumerate(item):
                if ind % 2 == 0:
                    test_key = re.findall(r"\s*((\"|\')([\w]+)\2)\s*", tok)
                    key_list.append(tok)
                else:
                    value_list.append(tok)
                    test_val = re.findall(r"\s*((\[[^\[\]]*\])|(\d+)|((\"\')([\w\@-])+\5))\s*", tok)

        for ind, tok in enumerate(key_list):
            test_key = re.findall(r"\s*((\"|\')([\w]+)\2)\s*", tok)
            print("token")
            print(tok)
            print("----------")
            if (test_key):
                print(test_key[0])

        for ind, tok in enumerate(value_list):
            test_val = re.findall(r"\s*((\[[^\[\]]*\])|(\d+)|((\"\')([\w\@-])+\5))\s*", tok)
            print("token")
            print(tok)
            print("----------")
            if test_val:
                print(test_val[0])
        print("+++++++++++++++++")

        if failed:
            return tmp_dict
        # for item in kwarg_tok:
        #     print(item)

        return tmp_dict


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
