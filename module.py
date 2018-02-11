import extra_functions.color as color


class Module():

    def __init__(self, opt, info = {}):
        """
        Example to create options and info in a custom module
        info = {
                "Name": "Module X",
                "Author": "Mr. X",
                "Description": "Exploit X" 
        }
        options = {
            "option1" : ["this option is ...", default_value, is_required?],
            "option2": ["...", "...", True]
        }
        """
        self.options = opt
        self.info = info
        self._init_check_module()
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
        print(color.BLUE + "[I] " + color.RESET + str(msg))

    def print_ok(self, msg):
        print(color.GREEN + "[OK] " +  color.RESET + str(msg))

    def print_error(self, msg):
        print(color.RED + "[KO] " +  color.RESET + str(msg))
    
    def _init_check_module(self):
        for k, v in self.options.items():
            if len(v) == 3:
                continue
            elif len(v) == 2:
                 self.options.get(k).append(True)
            else:
                raise Exception("Some option is wrong. Review the module\
                    \n Example: 'option': ['description', value, required?]")
        
    def check_module(self):
        try:
            for k,v in self.options.items():
                if not v[1] and v[2]:
                    raise Exception("%s is wrong. Use show options"%(k))
        except:
            raise Exception("Some option is wrong. Use show options")      

    # This function is called from shell - Run module
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
            print("The aren't options")
        for key, value in self.options.items():
            print(key + " (Required: %s)"%(value[2]))
            print("-"*len(key))
            print(" Description: ")
            print("  |--> " + value[0])
            print(" Value: ")
            aux_value = value[1]
            if type(aux_value) == type([]):
                for v in aux_value:
                    print("  |-->", v)
            else:
                print("  |--> ", aux_value)
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