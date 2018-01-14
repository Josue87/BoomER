from shell import Shell
from sys import exit
from os import _exit
from extra_functions.custom_print import error

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
