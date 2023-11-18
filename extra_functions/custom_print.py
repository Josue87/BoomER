import extra_functions.color as color


def error(msg):
    print(f"{color.RED}[KO] {color.RESET}{str(msg)}")


def ok(msg):
    print(f"{color.GREEN}[OK] {color.RESET}{str(msg)}")


def info(msg):
    print(f"{color.BLUE}[I] {color.RESET}{str(msg)}")
