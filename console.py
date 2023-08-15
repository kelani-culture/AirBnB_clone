#!/usr/bin/env python3
"""A module that implements the command line"""

from models.base_model import BaseModel
from models.console_utils import *
from models import storage
from models.user import User
import cmd
import re
import sys


def split_command_line_args(command_line):
    """split arguments logically using spaces"""
    pattern = r'"([^"]+)"|\'([^\']+)|\s+|(\S+)'
    args = [group for group in re.findall(pattern, command_line) if any(group)]
    if args:
        for idx, arg in enumerate(args):
            args[idx] = "".join(arg)
    return args


class HBNBCommand(cmd.Cmd):
    """Implementation of the command line
        intepreter"""
    prompt = "(hbnb) "

    def cmdloop(self):
        """handles CTRL+C"""
        try:
            super().cmdloop()
        except KeyboardInterrupt:
            print()

    def do_create(self, line):
        """this delegates the creation of new instances
            from passed in class names"""
        parsed = line.split()
        if len(parsed) == 1 and "." in parsed[0]:
            self.default(parsed)
            return
        handle_arg(1, "create", parsed, handle_create)

    def do_show(self, line):
        """this delegates the printing of string representation of
            an instance based on a class"""
        parsed = line.split()
        if len(parsed) == 1 and "." in parsed[0]:
            self.default(parsed)
            return
        handle_arg(2, "show", parsed, handle_show)

    def do_destroy(self, line):
        """this delegates the destruction of instances
            based on a class"""
        parsed = line.split()
        if len(parsed) == 1 and "." in parsed[0]:
            self.default(parsed)
            return
        handle_arg(2, "destroy", parsed, handle_destroy)

    def do_all(self, line):
        """this delegates the printing of all
            the instances in the storage engine"""
        parsed = line.split()
        if len(parsed) == 1 and "." in parsed[0]:
            self.default(parsed)
            return
        handle_arg(0, "all", parsed, handle_all)

    def do_update(self, line):
        """this delegates the updating of fields
            of the entries in the storage file"""
        parsed = split_command_line_args(line)
        if len(parsed) == 1 and "." in parsed[0]:
            self.default(str(parsed))
            return
        handle_arg(4, "update", parsed, handle_update)

    def do_quit(self, line):
        """exit handler for the cmd loop"""
        sys.exit()

    def do_EOF(self, line):
        """handles the CTRL+D key combs"""
        print()
        return True

    def default(self, line):
        """overrides the default behavior of the class when
            a wrong command format is parsed"""
        try:
            raw = re.findall(r"^(\w+)\.(\w+)\((.*)\)$", line)
        except TypeError:
            return
        if not raw:
            return
        cls_raw, method_raw, arg_raw = raw[0]
        if not parse_and_handle_arg(cls_raw, method_raw, arg_raw):
            return

    def emptyline(self):
        """handles the enter key"""
        pass

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

    def help_create(self):
        """this provides the description for the 'create' do-handler"""
        print("Usage:\t", end="")
        print("create <class name>")

    def help_show(self):
        """this provides the description for the 'show' do-handler"""
        print("Usage:\t", end="")
        print("show <class name> <id>")

    def help_all(self):
        """this provides the description for the 'all' do-handler"""
        print("Usage:\t", end="")
        print("all [<class name>]")

    def help_destroy(self):
        """this provides the description for the 'destroy' do-handler"""
        print("Usage:\t", end="")
        print("destroy <class name> <id>")

    def help_update(self):
        """this provides the description for the 'update' do-handler"""
        print("Usage:\t", end="")
        attr_name = "<attribute name>"
        attr_value = "<attribute value>"
        print(f"update <class name> <id> \"{attr_name}\" \"{attr_value}\"")

    def help_EOF(self):
        """display help information for the ^D keys"""
        print("\nUsage: CTRL+D\n")
        print("This command allows you to exit the cmd "
              "interpreter in a graceful manner\n")

    def help_quit(self):
        """
        Display help information for the quit command.
        """
        print("\nUsage: quit\n")
        print("This command allows you to exit the cmd "
              "interpreter.\n")
        print()


if __name__ == "__main__":
    HBNB_cmd = HBNBCommand()
    HBNB_cmd.cmdloop()
