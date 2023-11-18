from json import loads
from os.path import isdir

from requests import get

from module import Module


class BoomerModule(Module):
    def __init__(self):
        info = {
            "Name": "Software vulnerabilities",
            "Author": "Josue Encinar",
            "Description": "Find vulnerabilities in a SW"
        }
        options = {
            "software": ["Software to check (Don't use spaces)", "windows", True],
            "version": ["Software version", "10", False],
            "vendor": ["Software owner (Don't use spaces)", "microsoft", True],
            "directory": ["Directory to dump results", "files/output", False],
            "limit_result": ["Limit the number of results obtained (MAX: 100)", 25, False]
        }
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        self.write_file = False
        directory = self.options.get("directory")[1] or ""
        if directory and isdir(directory):
            self.write_file = True
        else:
            self.print_info("No file output")

        sw = self.options.get("software")[1]
        vendor = self.options.get("vendor")[1]
        version = self.options.get("version")[1]
        u_start = "http://cve.circl.lu/api/search/%s/%s_%s"
        url = u_start % (vendor.lower(), sw.lower(), version)
        name = f"{directory}/{sw}_{str(version)}.txt"
        try:
            # The API shows the version in different ways : _
            if self.request(url, name) == 0:
                u_start = u_start.replace("_", ":")
                url = u_start % (vendor.lower(), sw.lower(), version)
                self.request(url, name)
        except Exception as e:
            self.print_error(e)

    def request(self, url, name):
        self.print_info(f"Request to: {url}")
        ret = 1
        r = get(url)
        if r.status_code == 200:
            if data := loads(r.text):
                self.write_and_print_vulnerability_data(name, data)
            else:
                self.print_info(f"{url} -> No results...")
                ret = 0
        else:
            self.print_error("No response...")
        return ret

    # TODO Rename this here and in `request`
    def write_and_print_vulnerability_data(self, name, data):
        if self.write_file:
            f_out = open(name, "w")
            self.print_info(f"Opening {name}")
        i = 0
        total = str(len(data))
        self.print_ok(f"Total results: {total}" + "\n")
        for d in data:
            cve = d['id']
            cvss = str(d['cvss'])
            print(f"CVE: {cve}")
            print(f"CVSS: {cvss}" + "\n")
            if self.write_file:
                f_out.write("\nSummary: " + d['summary'] + "\n")
                f_out.write(f"CVE: {cve}" + "\n")
                f_out.write(f"CVSS: {cvss}" + "\n\n")
            i += 1
            if i in [self.options.get("limit_result")[1], 100]:
                self.print_info(
                    f"There are many results (only displayed {i} of {total})... stopping"
                )
                break
        if self.write_file:
            f_out.close()
