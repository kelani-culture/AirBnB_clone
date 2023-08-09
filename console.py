#!/usr/bin/python3
"""A module that implements the command line"""

from models.base_model import BaseModel
from models.engine.file_storage import storage
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


class HbnbCommand(cmd.Cmd):
    """Implementation of the command line
        intepreter"""
    prompt = "(hbnb) "

    def do_create(self, line):
        """this handles the creation of new instances
            from passed in class names"""
        parsed = line.split()

        def print_cls(cls_name):
            print("yea, i know this class :{}".format(cls_name))
        handle_arg(1, parsed, print_cls)

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
