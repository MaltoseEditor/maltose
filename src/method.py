import json
import os
import re
import shutil
import imghdr
import sys
import time
import traceback
from urllib.parse import unquote

import piexif

from src.customize import cprint
from src.customize.common import copy, getSummary, readfile, writefile, join, clear
from src.render import render_article, render_extends, render_info
from src.settings import BLOG_PATH, SOURCE_PATH, TIME_INDEX, TAGS_INDEX, CORPUS_INDEX, TEMPLATE_PATH
from src.datas import delete_aside, update_aside, index_corpus, index_tags, index_time, update_corpus, update_tags, update_time, update_xml


def __parse_img_path(path):
    """
    解析原始图片路径
    """
    if os.path.exists(path):
        return path
    path = unquote(path)
    if os.path.exists(path):
        return path
    if path[0] == "/":
        path = os.path.join(SOURCE_PATH, path[1:])
    else:
        path = os.path.join(SOURCE_PATH, path)
    if os.path.exists(path):
        return path
    return None


def __copy_img(path, each_img_tag, index):
    image = __parse_img_path(each_img_tag)
    if image is None:
        cprint.warning(f'The image "{each_img_tag}" is not found', index=2)
        return None
    else:
        new_image = f"{index}.{each_img_tag.split('.')[-1]}"
        cprint.green(f"Copy image '{image}' to '{new_image}'", index=2)
        copy(image, path, new_image)
        if imghdr.what(join(path, new_image)) in ("JPEG", "WebP"):
            piexif.remove(join(path, new_image))
    return new_image


def __check_datas(info):
    # 链接名不存在则终止此次保存
    if not info.get("permalink"):
        cprint.error(f"Fail: permalink must be seted！", index=1)
        return False

    # 链接不可出现 / 或 \
    if "/" in info["permalink"] or "\\" in info["permalink"]:
        cprint.error(f"Fail: permalink can't include '/' or '\'！", index=1)
        return False

    # 标题不存在则终止此次保存
    if not info.get("title"):
        cprint.error(f"Fail: title must be seted！", index=1)
        return False

    # 更新时间不存在则终止此次保存
    if not info.get("update"):
        cprint.error(f"Fail: update must be seted！", index=1)
        return False

    # 更新时间或者创建时间的格式不对则终止保存
    if info.get("date"):
        if re.match(r"\d{4}-\d{2}-\d{2}", info.get("date")) is None:
            return False
        if re.match(r"\d{4}-\d{2}-\d{2}", info.get("update")) is None:
            return False

    return True


def init_blog(article):
    file = os.path.join(SOURCE_PATH, article.replace(" ", "-") + ".md")
    if os.path.exists(file):
        sys.exit("The article is exists, please use other article name.")
    with open(file, "w", encoding="UTF-8") as md:
        md.write("""---
<title>{0}</title>
<date>{1}</date>
<update>{1}</update>
<tags></tags>
<corpus></corpus>
<permalink></permalink>
<summary></summary>
<recommend>false</recommend>
---

# {0}


""".format(article, time.strftime("%Y-%m-%d", time.localtime())))
    os.startfile(file)


def update_blog(article):
    try:
        with open(os.path.join(SOURCE_PATH, article.replace(" ", "-") + ".md"), "r", encoding="UTF-8") as md:
            markdown = md.read()
    except FileNotFoundError:
        cprint.error(
            f"The article is not found! Check the article name '{article}'")
        return

    cprint.blue(f'Parsing article "{article}"')
    try:
        info, markdown = render_info(markdown)
    except AttributeError:
        cprint.error("Fail: '---datas---' is not found!", index=1)
        traceback.print_exc()
        return

    if not __check_datas(info):
        return

    cprint.green(f"Rendering markdown to html", index=1)
    page = render_article(markdown, info)

    cprint.blue(f"Creating article directory '{info['permalink']}'", index=1)
    path = join(BLOG_PATH, "articles", info["permalink"])
    if not os.path.exists(path):
        os.makedirs(path)

    # create summary or not
    if info["summary"] == "":
        info["summary"] = getSummary(page)

    # 复制图片到对应文章目录下
    for index, each_img_tag in enumerate(re.findall(r'<img[\s\S]+?src="(?P<image>.*?)"', page)):
        if each_img_tag[:5] == "data:":
            continue
        new_path = __copy_img(path, each_img_tag, index)
        if new_path:
            page = re.sub(r'<img([\s\S]+?)src="{}"'.format(each_img_tag),
                          r'<img\g<1>src="{}"'.format(new_path), page)

    cprint.blue("Inserting the extend", index=1)
    page = render_extends(page, info)

    cprint.green('Creating the html file', index=1)
    writefile(os.path.join(path, "index.html"), page, encoding="UTF-8")

    cprint.green('Creating the json file', index=1)
    try:
        with open(os.path.join(path, "index.json"), "r+", encoding="UTF-8") as js:
            info_ = json.load(js)
            js.seek(0, 0)
            js.truncate()
            json.dump(info, js, indent=4)
        update_aside(info, info_)
    except FileNotFoundError:
        with open(os.path.join(path, "index.json"), "w", encoding="UTF-8") as js:
            json.dump(info, js, indent=4)
        update_aside(info)


def delete_blog(article):
    article = article.replace(" ", "-")
    path = os.path.join(BLOG_PATH, "articles")
    cprint.blue(f'Finding the article "{article}"...')
    for each in os.listdir(path):
        info = json.loads(readfile(os.path.join(
            path, os.path.join(each, "index.json"))))
        if article == info["title"]:
            shutil.rmtree(os.path.join(path, each))
            delete_aside(info)
            cprint.blue(f"Successfully deleted the article", index=1)
            break
    else:
        cprint.warning(
            f"Warning: The article: {article} is not found!", index=1)


def update_all_articles():
    for each in os.listdir(SOURCE_PATH):
        if each.split(".")[-1] == "md":
            update_blog(each.replace(".md", ""))


def update_all_aside():
    """清除原有的信息并全部重新生成"""
    cprint.blue("Clearing old datas...")
    clear(join(BLOG_PATH, "corpus"))
    if CORPUS_INDEX:
        copy(join(TEMPLATE_PATH, CORPUS_INDEX), join(BLOG_PATH, "corpus"), "index.html")
    clear(join(BLOG_PATH, "time"))
    if TIME_INDEX:
        copy(join(TEMPLATE_PATH, TIME_INDEX), join(BLOG_PATH, "time"), "index.html")
    clear(join(BLOG_PATH, "tags"))
    if TAGS_INDEX:
        copy(join(TEMPLATE_PATH, TAGS_INDEX), join(BLOG_PATH, "tags"), "index.html")

    writefile(join(BLOG_PATH, "index.html"), readfile(join(TEMPLATE_PATH, "index.html")))

    update_xml()

    for (root, dirs, _) in os.walk(join(BLOG_PATH, "articles")):
        if dirs:
            continue
        with open(join(root, "index.json")) as file:
            data = json.load(file)
        cprint.blue(f'Updating datas by "{data["title"]}"', index=1)
        update_time(data)
        update_corpus(data)
        update_tags(data)

    index_corpus()
    index_tags()
    index_time()
