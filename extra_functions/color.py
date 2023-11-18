from platform import platform

BLUE = f"{chr(27)}[0;34m"
GREEN = f"{chr(27)}[0;32m"
RED = f"{chr(27)}[0;31m"
YELLOW = f"{chr(27)}[0;33m"
RESET = f"{chr(27)}[0m"

pl = platform()
if "Windows" in pl and "Windows-10" not in pl:
    BLUE = ""
    GREEN = ""
    RED = ""
    YELLOW = ""
    RESET = ""
