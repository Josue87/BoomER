import os
from os import sep, walk
import readline
from extra_functions.load import loadModule
from extra_functions.autocomplete import MyCompleter
from extra_functions.record import start_record
from extra_functions.banner import banner
import extra_functions.custom_print as custom_print
from extra_functions.search import Search
import extra_functions.color as color


class Shell():
    def __init__(self):
        self.myModule = None
        self._options_start = {
            "load": "load <module> -> Load the module to use",
            "show":"show <modules_option> -> List modules availables",
            "search": "search <word> -> Search a word within info module",
            "help": "help -> Show this help",
            "clear": "clear -> Clear console log",
            "exit": "exit -> Exit BoomER"
        }
        start_record()  # To save records

    def prompt(self, module=None):
        if module is None:
            return "BoomER >> "
        else:
            return "BoomER" + color.RED + " |_" + color.YELLOW + str(module) + color.RED + "_|" + color.RESET + " >> "

    #This function is called with help command (argument are optional)
    def help(self, arg=""):
        if arg != "":
            aux = "Help to " + arg
            name = "help" + sep + "%s" + sep + arg + ".txt"
            try:
                file_open = name %("tool")
                f = open(file_open, 'r')
            except:
                try:
                    file_open = name %("modules")
                    f = open(file_open, 'r')
                    if not self.myModule:
                        custom_print.info("To see this help, first load a module")
                        return
                except:
                    custom_print.info(aux + " doesn't exist...")
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
            if(self.myModule is not None):
                self.myModule.help()

    #This function is called with load command
    def load(self, module):
        try:
            self.completer.remove_options(self.myModule.get_all_operations())
        except:
            pass
        module_load = loadModule(module)
        if(module_load is None):
            custom_print.error("Error loading module")
            return None
        custom_print.ok(str(module) + " loaded correctly")
        self.nameModule = module

        self.myModule = module_load
        try:
            self.completer.extend_completer(self.myModule.get_all_operations())
        except Exception as e:
            print(e)

    #This function is called whit show command
    def show(self, option):
        var = "modules"
        if "windows" in option:
            var = var + "/windows"
        elif "linux" in option:
            var = var + "/linux"
        elif "mac" in option:
            var = var + "/mac"
        elif "multi" in option:
            var = var + "/multi"
        elif "all" in option:
            pass
        elif ("options" in option or "info" in option) and self.myModule:
            self.myModule.show(option)
            return
        else:
            custom_print.error("show >> try with other option. " + option + " not found...")
            return

        for root, dirs, files in walk(var):
            for file in files:
                if ".py" == file[-3:] and file != "model.py" and file[0] != "_":
                    path = root.split(sep)[1:]
                    print(sep.join(path) + sep + file.split(".py")[0])  

    #Use to init completer 
    def initial(self):
        self.completer = MyCompleter(self._options_start.keys(), self)
        readline.set_history_length(50)  # max 50
        readline.set_completer_delims(' \t\n;')  # override the delims (we want /)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer.complete)

    def get_module(self):
        return self.myModule

    def start(self):
        self.initial()
        operation = ""
        banner()
        while True:
            if (self.myModule is None):
                operation = input(self.prompt())
            else:
                #to get name module
                ml = self.nameModule.split(sep)
                operation = input(self.prompt(ml[len(ml)-1]))
            op = operation.strip()
            op = self.strip_own(op)
            if (len(op) == 0):
                continue
            op[0] = op[0].lower()
            if(op[0] == "exit"):
                break
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
                raise Exception("Command " + op[0] + " not found. Try to load a module")
            else:
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
                    raise Exception("Command " + op[0] + " not found")

    #Remove current module
    def back(self):
        self.completer.remove_options(self.myModule.get_all_operations())
        self.myModule = None

    @staticmethod
    def strip_own(line):
        #Remove all "" in the list
        #Help to accept execution like this: put test    value
        mylist = line.split(" ")
        while "" in mylist:
            mylist.remove("")
        return mylist

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')