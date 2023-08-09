#!/usr/bin/python3
"""A module that implements the command line"""

import cmd
import sys


class HbnbCommand(cmd.Cmd):
    """Implementation of the command line
        intepreter"""
    prompt = "(hbnb) "

    def do_create(self, line):
        """this handles the creation of new instances
            from passed in class names"""
        print(line)

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
