#!/usr/bin/python3
"""Implement the command line"""

import cmd
import sys

class HbnbCommand(cmd.Cmd):
    """Implementation of the command line
    intepreter
    """
    cmd.Cmd.prompt = "(hbnb) "

    def do_quit(self, line):
        sys.exit()

    def help_quit(self):
        print("Quit command to exit the program")

    def do_EOF(self, line):
        return True




if __name__ == "__main__":
    Hbnb_cmd = HbnbCommand()
    Hbnb_cmd.cmdloop()
