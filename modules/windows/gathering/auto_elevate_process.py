import contextlib
from glob import glob
from multiprocessing.dummy import Pool
from os import walk, sep

from module import Module


class BoomerModule(Module):

    def __init__(self):
        info = {
            "Name": "Auto Elevate",
            "Author": "Josue Encinar",
            "Description": "Look for .exe with autoElevate true"
        }
        options = {
            "recursive": ["Check all files from option directory", False, False],
            "directory": ["Directory to check", "C:\\Windows\\System32\\", True],
            "file": ["File to dump results", "files\\output\\autoelevate.txt", True]
        }
        super(BoomerModule, self).__init__(options, info)

    def check_auto_elevate(self, pt):
        with contextlib.suppress(Exception):
            f = open(pt, 'rb')
            if b"<autoElevate>true</autoElevate>" in f.read():
                print(pt)
                return pt

    def run(self):
        files_to_check = []
        my_path = self.options["directory"][1]
        if not my_path.endswith(sep):
            my_path = my_path + sep
        f_open = self.options["file"][1]
        try:
            out_file = open(f_open, 'w')
        except Exception:
            self.print_error(f"Unable to create file: {f_open}")
            return
        self.print_info(f"Running through files from: {my_path}")
        if self.options["recursive"][1]:
            self.process_recursive_directory(my_path, files_to_check, out_file)
        else:
            f_exe = glob(f"{my_path}*exe")
            for f in f_exe:
                if self.check_auto_elevate(f):
                    out_file.write(f + "\n")
        out_file.close()

    # TODO Rename this here and in `run`
    def process_recursive_directory(self, my_path, files_to_check, out_file):
        self.print_info("Recursive mode")
        for b, d, f in walk(my_path):
            f_exe = glob(b + sep + "*exe")
            files_to_check.extend(f_exe)
        pool = Pool(8)
        results = pool.map(self.check_auto_elevate, files_to_check)
        pool.close()
        pool.join()
        for r in results:
            if r:
                out_file.write(r + "\n")
