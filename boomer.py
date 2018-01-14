from shell import Shell
from sys import exit
from os import _exit
from extra_functions.custom_print import error
from platform import system

if system() == "Windows":
    from ctypes import windll

    # Activate ANSI code on Windows
    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Boomer:
    @staticmethod
    def run():
        try:
            Shell().start()
        except KeyboardInterrupt:
            print("[!!] Bye BoomER")
            try:
                exit(0)
            except SystemExit:
                _exit(0)
        except Exception as e:
            error("Something was wrong...")
            error(e)

if __name__ == "__main__":
    Boomer.run()