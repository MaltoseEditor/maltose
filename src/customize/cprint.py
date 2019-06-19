from colorama import init
init(autoreset=True)


def __print_index(index: int, **kwargs):
    if kwargs.get("end"):
        kwargs.pop("end")
    if index == 1:
        print("  * ", end="", flush=True, **kwargs)
    elif index == 2:
        print("    - ", end="", flush=True, **kwargs)
    elif index == 3:
        print("      + ", end="", flush=True, **kwargs)


def printf(value, color=None, index=0, **kwargs):
    __print_index(index=index, **kwargs)
    if color is None:
        value = "\033[1;34;40m" + value + "\033[0m"
    elif color == "white":
        value = "\033[0m" + value + "\033[0m"
    elif color == "red":
        value = "\033[1;31;40m" + value + "\033[0m"
    elif color == "green":
        value = "\033[1;32;40m" + value + "\033[0m"
    elif color == "yellow":
        value = "\033[1;33;40m" + value + "\033[0m"
    else:
        raise AttributeError("The color is unexpected!")
    print(value, flush=True, **kwargs)


def normal(mes: str, index=0, **kwargs):
    printf(mes, color="white", index=index, **kwargs)


def green(mes: str, index=0, **kwargs):
    printf(mes, color="green", index=index, **kwargs)


def blue(mes: str, index=0, **kwargs):
    printf(mes, index=index, **kwargs)


def warning(mes: str, index=0, **kwargs):
    printf(mes, color="yellow", index=index, **kwargs)


def error(mes: str, index=0, **kwargs):
    printf(mes, color="red", index=index, **kwargs)
