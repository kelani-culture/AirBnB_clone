#!/usr/bin/env python3
"""A module that implements the command line"""

from models.base_model import BaseModel
from models.console_utils import *
from models import storage
from models.user import User
import cmd
import sys


class HbnbCommand(CompletionClass):
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

    def do_update(self, line):
        """this delegates the updating of fields
            of the entries in the storage file"""
        parsed = line.split()
        handle_arg(4, "update", parsed, handle_update)

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
