#!/usr/bin/python3
"""A module that implements the command line"""

from models.base_model import BaseModel
from models import storage
import cmd
import sys


def handle_arg(args, parsed, handler=None):
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
    if not handler:
        return
    if (not args):
        handler()

    if parsed:
        cls_name = parsed[0]
        if not (cls_name in globals()):
            print("** class doesn't exist **")
            return
    else:
        print("** class name missing **")
        return

    match args:
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
        res = res_objs[key]
    except KeyError:
        print("** no instance found **")
        return
    del res_objs[key]


class HbnbCommand(cmd.Cmd):
    """Implementation of the command line
        intepreter"""
    prompt = "(hbnb) "

    def do_create(self, line):
        """this delegates the creation of new instances
            from passed in class names"""
        parsed = line.split()
        handle_arg(1, parsed, handle_create)

    def do_show(self, line):
        """this delegates the printing of string representation of
            an instance based on a class"""
        parsed = line.split()
        handle_arg(2, parsed, handle_show)

    def do_destroy(self, line):
        """this destroy the destruction of instances
            based on a class"""
        parsed = line.split()
        handle_arg(2, parsed, handle_destroy)

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
