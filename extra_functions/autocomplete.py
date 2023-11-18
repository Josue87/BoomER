import contextlib
import os
import re

import readline


class MyCompleter():
    __instance = None

    @staticmethod
    def getInstance(commands=None, s=None):
        if commands is None:
            commands = []
        if MyCompleter.__instance is None:
            MyCompleter(commands, s)
        return MyCompleter.__instance

    def __init__(self, commands, s):
        if MyCompleter.__instance != None:
            raise Exception("This class is a singleton!")
        MyCompleter.__instance = self
        self.COMMANDS = []
        self.COMMANDS.extend(commands)
        self._c_reset = self.COMMANDS
        self.shell = s
        self.options_show = ["listeners", "multiModules", "windowsModules", "linuxModules", "macModules",
                             "allModules"]
        self._s_reset = self.options_show
        self.set_backup()
        self.all_payloads = []

    def set_all_payloads(self, p):
        self.all_payloads = p

    def set_all_commands(self, commands, show):
        self.COMMANDS = commands
        self.options_show = show

    def set_backup(self):
        self._auxCommands = self.COMMANDS
        self._auxShow = self.options_show

    def restore_backup(self):
        self.COMMANDS = self._auxCommands
        self.options_show = self._s_reset

    def reset(self):
        self.COMMANDS = self._c_reset
        self.options_show = self._auxShow

    def extend_completer(self, options):
        self.COMMANDS.extend(options)
        self.options_show = ["listeners", "multiModules", "windowsModules", "linuxModules", "macModules", "allModules",
                             "info", "options"]

    def remove_options(self, options):
        for option in options:
            with contextlib.suppress(Exception):
                self.COMMANDS.remove(option)
        self.options_show = ["listeners", "multiModules", "windowsModules", "linuxModules", "macModules", "allModules"]

    def _list_directories(self, root, route):
        my_list = []
        new_root = os.path.join(route, root)
        for name in os.listdir(new_root):
            if os.path.isdir(os.path.join(new_root, name)):
                name += os.sep
            if (name[0] != "_"):
                my_list.append(name.split(".py")[0])
        return my_list

    def _complete_path(self, path=None, route="modules"):
        if not path:
            return self._list_directories(".", route)
        directory = os.path.split(path)

        dir_tmp = directory[0] or "."
        my_list = [os.path.join(directory[0], new_path)
                   for new_path in self._list_directories(dir_tmp, route) if new_path.startswith(directory[1])]

        if len(my_list) > 1 or not os.path.exists(path):
            return my_list

        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._list_directories(path, route)]

        return [f'{path} ']

    def complete_load(self, args):
        if (len(args) > 1):
            return []
        path = os.path.join(".", "modules")
        if not args:
            return self._complete_path(route=path)

        return self._complete_path(args[-1], path)

    def complete_put(self, args):
        current_module = self.shell.get_module()
        if current_module is not None:
            if len(args) > 1 and args[0] == "payload":
                return self.complete_put_payload(args)
            options = list(current_module.get_options().keys())
            return [
                f'{option} '
                for option in options
                if (option.startswith(args[0].strip(" ")) and option != args[0])
            ]
        return ""

    def complete_listener(self, args):
        if (len(args) > 1):
            return []
        path = os.path.join(".", "listener")
        if not args:
            return self._complete_path(route=path)

        return self._complete_path(args[-1], path)

    # TODO
    def complete_put_payload(self, args):
        payloads = []
        for option in self.all_payloads:
            rest = "".join(args[1:])
            if ".pyc" not in option and (option.startswith(rest)):
                payloads.append(option)
        return payloads

    def complete_help(self, args):
        aux = list(self.shell._options_start.keys())
        if module := self.shell.get_module():
            aux.extend(list(module.get_all_operations()))
        return [
            f'{option} '
            for option in aux
            if (option.startswith(args[0].strip(" ")) and option != args[0])
        ]

    def complete_show(self, args):
        return [
            f'{option} '
            for option in self.options_show
            if (option.startswith(args[0].strip(" ")) and option != args[0])
        ]

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        line = buffer.split()

        if not line:
            return [f'{cmd} ' for cmd in self.COMMANDS][state]

        EXPR = re.compile('.*\s+$', re.M)

        if EXPR.match(buffer):
            line.append('')

        command = line[0].strip()

        if command in self.COMMANDS:
            command_function = getattr(self, f'complete_{command}')
            if args := line[1:]:
                return (command_function(args) + [None])[state]
            return [f'{command} '][state]
        results = [
                      f'{cmd} ' for cmd in self.COMMANDS if cmd.startswith(command)
                  ] + [None]

        return results[state]
