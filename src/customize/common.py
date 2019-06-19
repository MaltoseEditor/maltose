import os
import shutil
import time
import re
from html.parser import HTMLParser


class __Summary(HTMLParser):
    def __init__(self):
        self.text = ""
        super().__init__()

    def error(self, message):
        pass

    def handle_data(self, data):
        self.text += data


def getSummary(html):
    parser = __Summary()
    try:
        html = re.sub(r'<h1[\s\S]+?</h1>', "", html)
        html = re.sub(r'<script[\s\S]+?</script>', "", html)
        html = re.search(r"<body[\S\s]+</body>", html).group(0)
        parser.feed(html)
    except AttributeError:
        print(html)
        return ""
    datas = parser.text.strip()
    for i in range(50, len(datas)):
        if datas[i] in "。！\n":
            return datas[:i+1]
    return datas


def join(*args: str) -> str:
    path = "" + args[0]
    try:
        for each in args[1:]:
            path = os.path.join(path, each)
    except IndexError:
        raise AttributeError(
            'The parameters "args" expect at least two, but only one')
    return path


def clear(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def copy(file, path, filename=None):
    if filename is None:
        if not os.path.exists(path):
            os.makedirs(path)
        shutil.copy(file, path)
        return
    writefile(os.path.join(path, filename), readfile(file, True), True)


def readfile(file, byte=False, **kwargs) -> str:
    if byte:
        file = open(file, "rb", **kwargs)
    else:
        file = open(file, "r", **kwargs)
    data = file.read()
    file.close()
    return data


def writefile(file, data, byte=False, **kwargs) -> None:
    if byte:
        file = open(file, "wb", **kwargs)
    else:
        file = open(file, "w", **kwargs)
    file.write(data)
    file.close()


def getModifyTime(file: str):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(os.path.getmtime(file)))
