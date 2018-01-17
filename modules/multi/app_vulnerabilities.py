from requests import get
from os.path import isdir
from json import loads
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
        super(BoomerModule, self).__init__(options,info)
    
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
        u_start ="http://cve.circl.lu/api/search/%s/%s_%s"
        url = u_start%(vendor.lower(),sw.lower(),version)
        name =  directory + "/" + sw + "_" + str(version) + ".txt"
        try:
            # The API shows the version in different ways : _
            if self.request(url, name) == 0:
                u_start = u_start.replace("_", ":")
                url = u_start%(vendor.lower(),sw.lower(),version)
                self.request(url, name)
        except Exception as e:
            self.print_error(e)

    def request(self, url, name):
        self.print_info("Request to: " + url)
        ret = 1
        r = get(url)
        if r.status_code == 200:
            data = loads(r.text)
            if data:
                if self.write_file:
                    f_out = open(name, "w")
                    self.print_info("Opening " + name)
                i = 0
                total = str(len(data))
                self.print_ok("Total results: " + total + "\n")
                for d in data:
                    summary = d['summary'] 
                    cve = d['id']
                    cvss = str(d['cvss'])
                    print("CVE: " + cve)
                    print("CVSS: " + cvss + "\n")
                    if self.write_file:
                        f_out.write("\nSummary: " + summary + "\n")
                        f_out.write("CVE: " + cve + "\n")
                        f_out.write("CVSS: " + cvss + "\n\n")
                    i += 1
                    if (i == self.options.get("limit_result")[1]) or (i == 100):
                        self.print_info("There are many results (only displayed %s of %s)... stopping"%(str(i), total))
                        break
                if self.write_file:
                    f_out.close()
            else:
                self.print_info(url + " -> No results...")
                ret = 0
        else:
            self.print_error("No response...")
        return ret