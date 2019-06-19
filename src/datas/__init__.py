import re

from src.customize.common import join, readfile, writefile
from src.customize import cprint
from src.settings import BLOG_PATH, TEMPLATE_PATH

from .recommend import delete_rec, update_rec
from .corpus import update_corpus, delete_corpus, index_corpus
from .tags import update_tags, delete_tags, index_tags
from .time import update_time, delete_time, index_time
from .xml import update_rss, update_sitemap


def delete_aside(blog_info):
    cprint.blue(
        f'Delete corpus, tags, time from {blog_info["title"]}', index=1)
    delete_corpus(blog_info)
    delete_tags(blog_info)
    delete_time(blog_info)
    index_corpus()
    index_time()
    index_tags()
    update_xml()
    if blog_info["recommend"].lower() == "false":
        delete_rec(blog_info)


def update_aside(new: dict, old: dict = None):
    if old is None:
        cprint.blue(
            f'Create corpus, tags, time from {new["title"]}', index=1)
        update_corpus(new)
        update_tags(new)
        update_time(new)
    elif old == new:
        return
    else:
        delete_aside(old)
        if old["recommend"].lower() == "true":
            delete_rec(old)
        cprint.blue(
            f'Update corpus, tags, time from {new["title"]}', index=1)
        update_corpus(new)
        update_tags(new)
        update_time(new)
    index_corpus()
    index_time()
    index_tags()
    update_xml()
    if new["recommend"].lower() == "true":
        update_rec(new)


def update_xml():
    update_rss()
    update_sitemap()
