import contextlib
import os
from os import sep, walk

try:
    import readline
    import rlcompleter

    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except:
    pass
from sys import exit
from extra_functions.load import loadModule
from extra_functions.autocomplete import MyCompleter
from extra_functions.record import start_record
from extra_functions.banner import banner
import extra_functions.custom_print as custom_print
from extra_functions.search import Search
import extra_functions.color as color
from extra_functions.sessions.session import Session


class Shell():
    def __init__(self):
        self.myModule = None
        self._options_start = {
            "load": "load <module> -> Load the module to use",
            "show": "show <modules_option> -> List modules availables",
            "search": "search <word> -> Search a word within info module",
            "help": "help -> Show this help",
            "clear": "clear -> Clear console log",
            "sessions": "Show open sessions",
            "interact": "interact <session id> --> Interact with ID session",
            "exit": "exit -> Exit BoomER"
        }
        start_record()  # To save records

    # Use to init completer 
    def initial(self):
        self.completer = MyCompleter.getInstance(self._options_start.keys(), self)
        readline.set_history_length(50)  # max 50
        readline.set_completer_delims(' \t\n;')  # override the delims (we want /)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer.complete)
        self.open_sessions = Session.getInstance()

    def prompt(self, module=None):
        if module is None:
            return "BoomER >> "
        else:
            return f"BoomER{color.RED} |_{color.YELLOW}{str(module)}{color.RED}_|{color.RESET} >> "

    # This function is called with help command (argument are optional)
    def help(self, arg=""):
        if arg != "":
            aux = f"Help to {arg}"
            name = f"help{sep}%s{sep}{arg}.txt"
            try:
                file_open = name % ("tool")
                f = open(file_open, 'r')
            except Exception:
                try:
                    file_open = name % ("modules")
                    f = open(file_open, 'r')
                    if not self.myModule:
                        custom_print.info("To see this help, first load a module")
                        return
                except Exception:
                    custom_print.info(f"{aux} doesn't exist...")
                    return
            print("\n" + aux)
            print("-" * len(aux) + "\n")
            print(f.read() + "\n")
            f.close()
        else:
            print("\n--- Operations allowed ---\n")
            print("______   GLOBAL   _______")
            for key, value in self._options_start.items():
                if type(value) == type([]):
                    value = value[0]
                print(key + ":\n " + value)
            print("")
            if (self.myModule is not None):
                self.myModule.help()

    # This function is called with load command
    def load(self, module):
        with contextlib.suppress(Exception):
            self.completer.remove_options(self.myModule.get_all_operations())
        module_load = loadModule(module)
        if (module_load is None):
            custom_print.error("Error loading module")
            return None
        custom_print.ok(f"{str(module)} loaded correctly")
        self.nameModule = module
        self.myModule = module_load
        try:
            self.completer.extend_completer(self.myModule.get_all_operations())
        except Exception as e:
            print(e)

    # This function is called whit show command
    def show(self, option):
        var = "modules"
        if "windows" in option:
            var = var + sep + "windows"
        elif "linux" in option:
            var = var + sep + "linux"
        elif "mac" in option:
            var = var + sep + "mac"
        elif "multi" in option:
            var = var + sep + "multi"
        elif "all" in option:
            pass
        elif "listeners" in option:
            var = var + sep + "listener"
        elif ("options" in option or "info" in option) and self.myModule:
            self.myModule.show(option)
            return
        else:
            custom_print.error(f"show >> try with other option. {option} not found...")
            return

        for root, dirs, files in walk(var):
            for file in files:
                if file[-3:] == ".py" and file != "model.py" and file[0] != "_":
                    path = root.split(sep)[1:]
                    print(sep.join(path) + sep + file.split(".py")[0])

    def sessions(self):
        op_se = self.open_sessions.get_sessions()
        if len(op_se) == 0:
            print("No session (s) open")
            return
        for sid, data in op_se.items():
            addr = data[0].getpeername()
            print(f"{str(sid)} -> {addr[0]}:{str(addr[1])} -- {data[1]}")

    def interact(self, id=None):
        if not id:
            custom_print.error("It's necessary an ID")
            return
        self.open_sessions.interact(id)

    def get_module(self):
        return self.myModule

    def start(self):
        self.initial()
        banner()
        self.treat_input()

    def treat_input(self):
        operation = ""
        while True:
            if (self.myModule is None):
                operation = input(self.prompt())
            else:
                # to get name module
                ml = self.nameModule.split(sep)
                operation = input(self.prompt(ml[len(ml) - 1]))
            op = operation.strip()
            op = self.strip_own(op)
            if (len(op) == 0):
                continue
            op[0] = op[0].lower()
            if (op[0] == "exit"):
                print("Closing BoomER")
                exit(0)
            try:
                self.exec_command(op)
            except Exception as e:
                custom_print.error(e)

    def exec_command(self, op):
        if op[0] == "search":
            if len(op) == 1:
                custom_print.error("What do you want to search?")
            else:
                Search().search(op[1:])
        elif op[0] == "back":
            self.back()
        elif op[0] == "clear":
            self.clear()
        elif op[0] in self._options_start.keys():
            if len(op) == 1:
                getattr(self, op[0])()
            elif len(op) >= 2:
                getattr(self, op[0])(op[1])
        else:
            if not self.myModule:
                raise Exception(f"Command {op[0]} not found. Try to load a module")
            if op[0] in self.myModule.get_single_operations():
                # before run --> check if all options have a correct value
                if op[0] == "run":
                    self.myModule.check_module()
                getattr(self.myModule, op[0])()
            elif op[0] in self.myModule.get_parameter_operations():
                if len(op) >= 2:
                    getattr(self.myModule, op[0])(op[1])
                else:
                    raise Exception("positional argument")
            elif op[0] in self.myModule.get_multiple_parameter_operations():
                if len(op) >= 2:
                    getattr(self.myModule, op[0])(op[1:])
                else:
                    raise Exception("positional argument")
            else:
                raise Exception(f"Command {op[0]} not found")

    # Remove current module
    def back(self):
        self.completer.reset()
        self.myModule = None

    @staticmethod
    def strip_own(line):
        # Remove all "" in the list
        # Help to accept execution like this: put test    value
        mylist = line.split(" ")
        while "" in mylist:
            mylist.remove("")
        return mylist

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
