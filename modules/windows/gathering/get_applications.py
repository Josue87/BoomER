import contextlib
import winreg

from module import Module


class BoomerModule(Module):

    def __init__(self):
        info = {
            "Name": "Windows App Finder",
            "Author": "Josue Encinar",
            "Description": "Find applications installed on Windows"
        }
        options = {
            "hk": ["Select Key:\n   0 -> Current User\n   1 -> Local Machine", 1, True],
            "file": ["File to dump results", "files/output/win_app_finder.txt", False]
        }
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        self.file_open = None
        if f := self.options.get("file")[1]:
            try:
                self.file_open = open(self.options.get("file")[1], "w")
            except Exception as e:
                self.print_error(e)
                self.print_info("Only displayed by the console.")
        hk_option = int(self.options.get("hk")[1])
        if hk_option in {0, 1}:
            regkeys = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
            self.search_register(hk_option, regkeys)
            regkeys_wow = "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
            with contextlib.suppress(Exception):
                self.search_register(hk_option, regkeys_wow)
        else:
            self.print_error("Invalid hk option")
        if self.file_open:
            self.file_open.close()

    def search_register(self, option_hk, key_path):
        if option_hk == 0:
            h_key = winreg.HKEY_CURRENT_USER
            data = "HKEY_CURRENT_USER -> "
        else:
            h_key = winreg.HKEY_LOCAL_MACHINE
            data = "HKEY_LOCAL_MACHINE -> "
        self.print_info(data + key_path)
        if self.file_open:
            self.file_open.write("\n" + data + key_path + "\n\n")
        key = winreg.OpenKey(h_key, key_path, 0, winreg.KEY_READ)
        for subkey in self.get_subkeys(key):
            subkey_path = "%s\\%s" % (key_path, subkey)
            self.get_apps_values(h_key, subkey_path)
        winreg.CloseKey(key)

    def get_subkeys(self, key):
        i = 0
        my_list = []
        while True:
            try:
                subkey = winreg.EnumKey(key, i)
                my_list.append(subkey)
                i += 1
            except WindowsError as e:
                break
        return my_list

    def get_apps_values(self, h_key, key_path):
        key = winreg.OpenKey(h_key, key_path, 0, winreg.KEY_READ)
        i = 0
        name = ""
        version = "???"
        while True:
            try:
                subkey = winreg.EnumValue(key, i)
                result = subkey[0]
                if result == "DisplayName":
                    name = subkey[1]
                elif result == "DisplayVersion":
                    version = subkey[1]
                i += 1
            except WindowsError as e:
                break
        if name != "":
            data = f"{name} ---> {version}"
            print(data)
            if self.file_open:
                self.file_open.write(data + "\n")
        winreg.CloseKey(key)
