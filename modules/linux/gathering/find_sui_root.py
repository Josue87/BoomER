from module import Module
from stat import S_ISUID, S_ISGID
from os import stat, listdir, walk
from os.path import isfile, join
from multiprocessing.dummy import Pool

class BoomerModule(Module):
    def __init__(self):
        info = {"Name": "SUID Root files",
                "Author": "Josue Encinar",
                "Description": "Module to find files with setuid Root",
        }
        options = {
            "recursive": ["Check all files from option directory", True],
            "directory": ["Directory to check", "/"],
            "file": ["File to dump results", "files/output/suid_sgid_root.txt"]
        }
        super(BoomerModule, self).__init__(options,info)
        
    def run(self):
        file_w = open(self.options["file"][1], "w")
        my_dir = self.options["directory"][1]
        if not my_dir.endswith("/"):
            my_dir = my_dir + "/"
        results = self.recursive(my_dir) if self.options["recursive"][1]\
                 else self.no_recursive(my_dir)
        suid = results[0]
        sgid = results[1]

        file_w.write("__SUID ROOT ACTIVE__\n")
        for f_suid in suid:
            file_w.write(f_suid + "\n")
        file_w.write("__SGID ROOT ACTIVE__\n")
        for f_sgid in sgid:
            file_w.write(f_sgid + "\n")
        file_w.close()
        self.print_ok("Check the file " + self.options["file"][1] + " to view the results")

    def no_recursive(self, my_dir):
        files_suid = []
        files_sgid = []
        for f in listdir(my_dir):
            aux_file = join(my_dir, f)
            if isfile(aux_file):
                result = self.is_suid_sgid(aux_file)
                if result[0]:
                    files_suid.append(result[0])
                if result[1]:
                    files_sgid.append(result[1])
        return [files_suid, files_sgid]

    def recursive(self, my_dir):
        self.print_info("Recursive mode")
        files_suid = []
        files_sgid = []
        files_list = []
        for cpwd, dirs, files in walk(my_dir):
            if cpwd.endswith("/"):
                cwd = cpwd
            else:
                cwd = cpwd + "/"
            for f in files:
                files_list.append(cwd + f)
        pool = Pool(8)
        results = pool.map(self.is_suid_sgid, files_list)
        pool.close()
        pool.join()
        for result in results:
            if result[0]:
                files_suid.append(result[0])
            if result[1]:
                files_sgid.append(result[1])

        return [files_suid, files_sgid]

    def is_suid_sgid(self, file_name):
        results = []
        try:
            f = stat(file_name)
            mode = f.st_mode
        except:
            return [None, None]
        if (mode & S_ISUID) == 2048:
            print("SUID: " + file_name)
            results.append(file_name)
        else:
            results.append(None)

        if (mode & S_ISGID) == 1024:
            print("SGIG: " + file_name)
            results.append(file_name)
        else:
            results.append(None)

        return results