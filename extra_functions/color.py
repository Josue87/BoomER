from platform import platform

BLUE = chr(27) + "[0;34m"
GREEN = chr(27) + "[0;32m"
RED = chr(27) + "[0;31m"
YELLOW = chr(27) + "[0;33m"
RESET = chr(27) + "[0m"

pl = platform()
if "Windows" in pl and not "Windows-10" in pl:
    BLUE = ""
    GREEN = ""
    RED = ""
    YELLOW = ""
    RESET = ""