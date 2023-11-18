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
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        self.file_open = None
        if f := self.options.get("file")[1]:
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
        return self.extract_info_by_prefix(data, "Version=")

    def _get_name(self, data):
        return self.extract_info_by_prefix(data, "Name=")

    # TODO Rename this here and in `_get_version` and `_get_name`
    def extract_info_by_prefix(self, data, arg1):
        v = data.split(arg1)
        return v[1].split("\n")[0] if len(v) > 1 else None

    def find_apps(self, dir):
        for app in listdir(dir):
            with open(f"{dir}/{app}", "r") as f:
                data = f.read()
            name = self._get_name(data)
            version = self._get_version(data) or "??"
            if name and version:
                to_print = f"{name} ---> {version}"
                print(to_print)
                if self.file_open:
                    self.file_open.write("\n" + to_print + "\n")
