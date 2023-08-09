#!/usr/bin/python3
"""A module that implements the command line"""

from models.base_model import BaseModel
from models import storage
import cmd
import sys


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
                instance = parsed[1]
            except IndexError:
                print("** instance id missing **")
                return
            handler(cls_name, instance)
        case _:
            pass


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
    for key, value in res_insts.items():
        class_str = key.split(".")[0]
        instance = globals()[class_str](**value)
        res_insts[key] = instance.__str__()
    res_array = [value for key, value in res_insts.items()]
    print(res_array)


class HbnbCommand(cmd.Cmd):
    """Implementation of the command line
        intepreter"""
    prompt = "(hbnb) "

    def do_create(self, line):
        """this delegates the creation of new instances
            from passed in class names"""
        parsed = line.split()
        handle_arg(1, "create", parsed, handle_create)

    def do_show(self, line):
        """this delegates the printing of string representation of
            an instance based on a class"""
        parsed = line.split()
        handle_arg(2, "show", parsed, handle_show)

    def do_destroy(self, line):
        """this delegates the destruction of instances
            based on a class"""
        parsed = line.split()
        handle_arg(2, "destroy", parsed, handle_destroy)

    def do_all(self, line):
        """this delegates the printing of all
            the instances in the storage engine"""
        parsed = line.split()
        handle_arg(0, "all", parsed, handle_all)

    def do_quit(self, line):
        """exit handler for the cmd loop"""
        sys.exit()

    def help_quit(self):
        """provides guide for the quit command"""
        print("Quit command to exit the program")

    def do_EOF(self, line):
        """handles the CTRL+D key combs"""
        return True


if __name__ == "__main__":
    Hbnb_cmd = HbnbCommand()
    Hbnb_cmd.cmdloop()
