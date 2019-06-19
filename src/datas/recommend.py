import os

from src.settings import BLOG_PATH
from src.customize.common import join

from .common import _update_data_json, _delete_data_json


def update_rec(info: dict):
    recommend = join(BLOG_PATH, "recommend")
    if not os.path.exists(recommend):
        os.mkdir(recommend)
    _update_data_json(recommend, info)


def delete_rec(info: dict):
    recommend = join(BLOG_PATH, "recommend")
    if not os.path.exists(recommend):
        os.mkdir(recommend)
        return
    _delete_data_json(recommend, info)
