import abc
import extra_functions.color as color


class Module(metaclass=abc.ABCMeta):

    def __init__(self, opt, info = {}):
        self.options = opt
        self.info = info
        # This is for options that permit use the module (after call super init)
        self.module_parameter_operations = {}
        self.module_multiple_parameter_operations = {
            "put": "put <option> value_option -> Configure module options.\
             \n You can see module options with 'show options'",
            }
        self.module_single_operations = { 
                        "run": "run -> Execute the module",
                        "check": "check -> Check if the OS is vulnerable", 
                        "back": "back -> Unload module"
                        }
    
    #The following 3 options are to print messages
    def print_info(self, msg):
        print(color.BLUE + "[*] " + color.RESET + str(msg))

    def print_ok(self, msg):
        print(color.GREEN + "[+] " +  color.RESET + str(msg))

    def print_error(self, msg):
        print(color.RED + "[-] " +  color.RESET + str(msg))
        
    def check_module(self):
        try:
            for v in self.options.values():
                if v[1]:
                    continue
                else:
                    raise Exception("Some option is wrong. Use show options")
        except:
            raise Exception("Some option is wrong. Use show options")      

    # This function is called from shell - Run module
    @abc.abstractmethod
    def run(self):
        raise Exception("Module doesn't implement run function...") 

    # Function to check if the system is vulnerable
    def check(self):
        raise Exception("This module does not support check functionality")

    def get_options(self):
        return self.options

    def show(self, option):
        option = option.lower()
        if option == "info":
            self.print_module_info()
        elif option == "options":
            self.print_options()
        else:
            print("Bad parameter to show")
    
    #This function is used to set a value in an option
    def put(self, args):
        try:
            self.options[args[0]][1] = ' '.join(args[1:])
            self.print_info(args[0] + " => " + ' '.join(args[1:]))
        except:
            self.print_error("Option: " + args[0] +" not found")

    def print_options(self):
        print(color.YELLOW + "\n.. OPTIONS .." + color.RESET)
        print("__________________________________________________________________\n")
        if not len(self.options):
            print("Thre aren't options")
        for key, value in self.options.items():
            print(key)
            print("-"*len(key))
            print(" Description: ")
            print("  |--> " + value[0])
            print(" Value: ")
            i = 1
            while i < len(value):
                print("  |--> " + str(value[i]))
                i += 1
        print("__________________________________________________________________\n")
        
    def print_module_info(self):
        print(color.YELLOW + "\n.. MODULE INFORMATION  .." + color.RESET)
        print("__________________________________________________________________\n")
        if not len(self.info):
            print("No info to show")
        for key, value in self.info.items():
            print(key)
            print("-"*len(key))
            print("  |--> " + str(value))
        print("__________________________________________________________________\n")

    #This function is called in main script to show help
    def help(self):
        print("______   MODULE   _______")
        for op, des in self.module_single_operations.items():
            if des == "":
                des = "No description..."
            print(op + ":\n " + des)
        for op, des in self.module_parameter_operations.items():
            if des == "":
                des = "No description..."
            print(op + ":\n " + des)
        for op, des in self.module_multiple_parameter_operations.items():
            if des == "":
                des = "No description..."
            print(op + ":\n " + des)
        print("show:\n show <options | info>  -> Shows the module options or module info")
        print("")

    #The following functions return allowed operations
    def get_single_operations(self):
        return self.module_single_operations.keys()

    def get_parameter_operations(self):
        return self.module_parameter_operations.keys()
    
    def get_multiple_parameter_operations(self):
        return self.module_multiple_parameter_operations.keys()
    
    def get_all_operations(self):
        return list(self.get_multiple_parameter_operations())\
            + list(self.get_parameter_operations())\
                + list(self.get_single_operations())

    # If a module needs more operations, use the following functions
    # Remember!! You enter new operations after calling up super in the init function.
    # Operation without arguments
    def register_single_operation(self, op, description=""):
        if op != "" and not self._exists(op.lower()):
            self.module_single_operations[op.lower()] = description

    # Operation with a parameter
    def register_parameter_operation(self, op, description=""):
        if op != "" and not self._exists(op.lower()):
            self.module_parameter_operations[op.lower()] = description
    
    # Operation with multiple parameters
    def register_multiple_parameter_operation(self, op, description=""):
        if op != "" and not self._exists(op.lower()):
            self.module_multiple_parameter_operations[op.lower()] = description
    
    def _exists(self, op):
        return op in self.module_single_operations\
                or op in self.module_parameter_operations\
                or op in self.module_multiple_parameter_operations

    # If a module doesn't need an operation, use this function to delete it
    def deregister_operation(self, op):
        try:
            del self.module_single_operations[op]
        except:
            try:
                del self.module_parameter_operations[op]
            except:
                try:
                    del self.module_multiple_parameter_operations[op]
                except Exception as e:
                    print(e)