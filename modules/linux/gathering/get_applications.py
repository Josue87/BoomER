from os import listdir
from module import Module

class BoomerModule(Module):

    def __init__(self):
        info = {
                "Name": "Linux App Finder",
                "Author": "Josue Encinar",
                "Description": "Find applications installed on Linux" 
        }
        options = {
            "file": ["File to dump results", "files/output/linux_app_finder.txt", False]
        }
        super(BoomerModule, self).__init__(options,info)
    
    def run(self):
        self.file_open = None
        f = self.options.get("file")[1]
        if f:
            try:
                self.file_open = open(self.options.get("file")[1], "w")
            except Exception as e:
                self.print_error(e)
                self.print_info("Only displayed by the console.")

        dir = "/usr/share/applications"
        self.find_apps(dir)
        if self.file_open:
            self.file_open.close()

    def _get_version(self, data):
        v = data.split("Version=")
        version = None
        if len(v) > 1:
            version = v[1].split("\n")[0]
        return version

    def _get_name(self, data):
        v = data.split("Name=")
        version = None
        if len(v) > 1:
            version = v[1].split("\n")[0]
        return version
            
    def find_apps(self, dir):
        for app in listdir(dir):
            #print(dir+"/"+app)
            f = open(dir+"/"+app, "r")
            data = f.read()
            f.close()
            name = self._get_name(data)
            version = self._get_version(data)
            if not version:
                version = "??"
            if name and version:
                to_print = name + " ---> " + version
                print(to_print)
                if self.file_open:
                    self.file_open.write("\n" + to_print + "\n")