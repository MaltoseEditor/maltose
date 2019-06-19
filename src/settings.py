import os
import sys
import time
import json
import threading

from .customize import cprint

MALTOSE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(MALTOSE_PATH, "Templates")
VERSION = "Maltose-0.3.0"
PREVIEW_PORT = 80
DEFAULT_CORPUS = ""
TIME_INDEX = ""
TAGS_INDEX = ""
CORPUS_INDEX = ""
TEMPLATE_CORPUS = "corpus"
TEMPLATE_TAG = "tag"
TEMPLATE_TIME = "time"
BLOG_PATH = ""
SOURCE_PATH = ""
AUTHOR = ""
WEBSITE = ""
TITLE = ""
DESCRIPTION = ""
PLUGINS = None
CMD_LIST = []

try:
    with open(os.path.join(MALTOSE_PATH, "config.json"), "r", encoding="UTF-8") as _Config:
        _data = json.load(_Config)

        for key, value in _data.items():
            locals()[key.upper()] = value

except FileNotFoundError:
    cprint.error("The config.json not found")
    cprint.blue("Creating the config.json in root directory.")
    cprint.blue(
        "If you want to create config.json by yourself, press Ctrl+C to quit.")
    try:
        _data = dict()
        _data["BLOG_PATH"] = input("Your blog directory path: ")
        _data["SOURCE_PATH"] = input(
            "Your markdown files directory path: ")
        _data["TITLE"] = input("Your blog title: ")
        _data["WEBSITE"] = input(
            "Your blog link(like=> https://abersheeran.com): ")
        _data["AUTHOR"] = input("Your nickname in blog: ")

        with open(os.path.join(MALTOSE_PATH, "config.json"), "w", encoding="UTF-8") as _Config:
            json.dump(_data, _Config)

        for key, value in _data.items():
            locals()[key.upper()] = value

    except KeyboardInterrupt:
        cprint.green("\r\nCancel to create config.json.")
        sys.exit()


class Check():
    """检查必要的配置"""

    def __init__(self):
        self.run()

    @staticmethod
    def CheckTemplate():
        if not os.path.exists(os.path.join(TEMPLATE_PATH, "index.html")):
            cprint.error(f"The index.html in {TEMPLATE_PATH} not found!")
            sys.exit()
        if not os.path.exists(os.path.join(TEMPLATE_PATH, f"{TEMPLATE_CORPUS}.html")):
            cprint.error(f"The {TEMPLATE_CORPUS}.html in {TEMPLATE_PATH} not found!")
            sys.exit()
        if not os.path.exists(os.path.join(TEMPLATE_PATH, f"{TEMPLATE_TAG}.html")):
            cprint.error(f"The {TEMPLATE_TAG}.html in {TEMPLATE_PATH} not found!")
            sys.exit()
        if not os.path.exists(os.path.join(TEMPLATE_PATH, f"{TEMPLATE_TIME}.html")):
            cprint.error(f"The {TEMPLATE_TIME}.html in {TEMPLATE_PATH} not found!")
            sys.exit()
        if not os.path.exists(os.path.join(TEMPLATE_PATH, "article.html")):
            cprint.error(f"The article.html in {TEMPLATE_PATH} not found!")
            sys.exit()

    @staticmethod
    def CheckTarget():
        if not os.path.exists(BLOG_PATH):
            cprint.error("Blog_path %s is not found!" % BLOG_PATH)
            sys.exit()

    @staticmethod
    def CheckSource():
        if not os.path.exists(SOURCE_PATH):
            cprint.error("Source_path %s is not found!" % SOURCE_PATH)
            sys.exit()

    @staticmethod
    def CheckInfomations():
        if WEBSITE == "":
            cprint.error("In settings: Website must be seted!")
            sys.exit()

    def run(self):
        for check in filter(lambda func: func.startswith("Check") and callable(getattr(self, func)), dir(self)):
            getattr(self, check)()
