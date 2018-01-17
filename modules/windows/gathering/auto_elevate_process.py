from module import Module
from os import walk, sep
from glob import glob
from multiprocessing.dummy import Pool

class BoomerModule(Module):

    def __init__(self):
        info = {
                "Name": "Auto Elevate",
                "Author": "Josue Encinar",
                "Description": "Look for .exe with autoElevate true" 
        }
        options = {
            "recursive": ["Check all files from option directory", False, False],
            "directory": ["Directory to check", "C:\Windows\System32\\", True],
            "file": ["File to dump results", "files/output/autoelevate.txt", True]
        }
        super(BoomerModule, self).__init__(options,info)
    
    def check_auto_elevate(self, pt):
        try:
            f = open(pt,'rb')
            if b"<autoElevate>true</autoElevate>" in f.read():
                print(pt)
                return pt            
        except Exception as e:
            pass

    def run(self):
        files_to_check = []
        my_path = self.options["directory"][1]
        if not my_path.endswith(sep):
            my_path = my_path + sep
        f_open = self.options["file"][1]
        try:
            out_file = open(f_open, 'w')
        except:
            self.print_error("Unable to create file: " + f_open)
            return
        self.print_info("Running through files from: " + my_path)
        if self.options["recursive"][1]:
            self.print_info("Recursive mode")
            for b, d, f in walk(my_path):
                f_exe = glob(b + sept + "*exe")
                files_to_check.extend(f_exe)
            pool = Pool(8)
            results = pool.map(self.check_auto_elevate, files_to_check)
            pool.close()
            pool.join()
            for r in results:
                if r:
                    out_file.write(r + "\n")
        else:
            f_exe = glob(my_path + "*exe")
            for f in f_exe:
                if self.check_auto_elevate(f):
                    out_file.write(f + "\n")
        out_file.close()