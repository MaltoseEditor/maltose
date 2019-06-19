import os
import sys
from getopt import getopt

from .method import (
    delete_blog,
    update_blog,
    init_blog,
    update_all_articles,
    update_all_aside
)
from .customize import cprint, common
from .settings import BLOG_PATH, VERSION, CMD_LIST, Check
from .preview import main as _preview


def getOption(short: str, long: list = None, argv: list = sys.argv[2:]) -> dict:
    result = dict()
    if long is None:
        opts, args = getopt(argv, short)
    else:
        opts, args = getopt(argv, short, long)
    for key, value in opts:
        result[key] = value
    result["args"] = args
    return result


def push():
    os.chdir(BLOG_PATH)
    os.system("git pull")
    os.system("git add .")
    os.system(f'git commit -m "Auto update by {VERSION}"')
    os.system('git push')


def new():
    article = sys.argv[2]
    init_blog(article)


def update():
    article = sys.argv[2]
    update_blog(article)


def delete():
    article = sys.argv[2]
    delete_blog(article)


def preview():
    opts = getOption("s")
    isSlow = True
    if opts.get("-s") is None:
        isSlow = False
    _preview(isSlow=isSlow)


def update_all():
    common.clear(common.join(BLOG_PATH, "articles"))
    update_all_articles()
    update_all_aside()


def cmd():
    os.chdir(BLOG_PATH)
    cmd_list = CMD_LIST
    try:
        num = int(sys.argv[2])
        os.system(cmd_list[num])
        return
    except IndexError:
        pass
    except ValueError:
        pass
    cprint.normal("Select one to run, input Ctrl+C to quit:")
    for index, item in enumerate(cmd_list):
        cprint.blue(f"  {index}: {item}")
    try:
        num = int(input("Input the line num: "))
    except KeyboardInterrupt:
        cprint.green("Cancel.")
        return
    if num < -1 or num >= len(cmd_list):
        cprint.error("Over index.")
        return
    elif num == -1:
        cprint.green("Cancel.")
        return
    os.system(cmd_list[num])


methods = {
    "new": [
        new,
        "Create new template markdown file in SOURCE_PATH"
    ],
    "update": [
        update,
        "Update the article from SOURCE_PATH"
    ],
    "delete": [
        delete,
        "Delete the article from BLOG_PATH. But the will not remove or change the SOURCE FILE, so if you want remove article forever, you must remove the article's markdown file or remove the article's permalink data."
    ],
    "update-all": [
        update_all,
        "Clear directory 'articles' and call methods `render-all` and `write-all`."
    ],
    "render-all": [
        update_all_articles,
        "Render all articles. The methods will not remove directory 'articles'."
    ],
    "write-all": [
        update_all_aside,
        "Remove directories 'time', 'tags', 'corpus'. And then create data from directory 'articles'."
    ],
    "push": [
        push,
        "Push your blog. You must have git in your PC to use it."
    ],
    "preview": [
        preview,
        "Start the preview server for your blog. Can use the argument `-s` to set the server be s..l..o..w.."
    ],
    "cmd": [
        cmd,
        "Select one command to run."
    ]
}


def main():
    try:
        method = sys.argv[1]
    except IndexError:
        method = input("Input operation: ")
    if methods.get(method) is None:
        if method != "help":
            cprint.error("Error: Wrong operation!")
        cprint.blue("You can only use the follow operation:")
        for key, value in methods.items():
            cprint.green(key, index=1, end=" ")
            cprint.blue(value[1])
    else:
        methods[method][0]()

Check()
